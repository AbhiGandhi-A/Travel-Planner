import smtplib
import mysql.connector
from flask import Flask, render_template, request, jsonify, abort
from flask_cors import CORS
from flask_mysqldb import MySQL
import random
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from dateutil.parser import parse
from flask_mysqldb import MySQLdb, cursors

app = Flask(__name__)
CORS(app)

# MySQL Config
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Abhi@3014A'
app.config['MYSQL_DB'] = 'user'

# Update your database configuration here
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Abhi@3014A',
    'database': 'user',  # Replace with your actual database name
    'port': 3306
}

# Flask-Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'garbahub88@gmail.com'  # Update with your Gmail email
app.config['MAIL_PASSWORD'] = 'gznl jxfn erge qizt'  # Update with your generated app password

mail = Mail(app)
mysql = MySQL(app)


# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))


@app.route('/')
def index():
    return render_template('index1.html')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                        (username, password, email))
            mysql.connection.commit()

        return jsonify({'message': 'User registered successfully!'})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        print(f"Attempting login for username: {username}")

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()

        print(f"user: {user}")

        if user:
            print("Login successful!")
            return jsonify({'message': 'Login successful!', 'redirect': '/index1'})
        else:
            print("Invalid credentials")
            return jsonify({'error': 'Invalid credentials'})

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'error': 'Login failed. Please try again.'})


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        email = request.form['email']

        # Check if the email exists in the database
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

        if user:
            # Generate OTP
            otp = generate_otp()

            # Update the user's record in the database with the OTP
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE users SET otp = %s WHERE email = %s", (otp, email))
                mysql.connection.commit()

            # Send OTP via email
            send_otp_via_email(email, otp)

            return jsonify({'message': 'OTP sent to your email for password reset'})

        else:
            return jsonify({'error': 'Email not found'})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        email = request.form['email']
        otp = request.form['otp']
        new_password = request.form['new_password']

        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s AND otp = %s", (email, otp))
            user = cur.fetchone()

            if user:
                cur.execute("UPDATE users SET password = %s, otp = NULL WHERE email = %s", (new_password, email))
                mysql.connection.commit()

                return jsonify({'message': 'Password reset successful'})

            else:
                return jsonify({'error': 'Invalid email or OTP'})

    except Exception as e:
        return jsonify({'error': str(e)})


def send_otp_via_email(receiver_email, otp):
    sender_email = app.config['MAIL_USERNAME']

    subject = "Password Reset OTP"
    body = f"Your OTP for password reset is: {otp}"

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, app.config['MAIL_PASSWORD'])
        server.sendmail(sender_email, receiver_email, msg.as_string())


@app.route('/get_travel_planning', methods=['POST'])
def get_travel_planning():
    try:
        selected_destination = request.json.get('destination')
        budget_str = request.json.get('budget')
        from_date_str = request.json.get('fromDate')
        to_date_str = request.json.get('toDate')

        # Validate input parameters
        if not all([selected_destination, budget_str, from_date_str, to_date_str]):
            return jsonify({'success': False, 'message': 'Invalid input. Please provide all required parameters.'})

        # Validate and parse date strings
        try:
            from_date = parse(from_date_str)
            to_date = parse(to_date_str)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format. Please provide valid date strings.'})

        # Convert budget string to float
        try:
            budget = float(budget_str)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid budget format. Please provide a valid number for the budget.'})

        # Fetch total expenses for the trip based on the selected destination and dates
        total_expenses = calculate_total_expenses(selected_destination, from_date, to_date)

        # Compare total expenses with the user's budget
        if total_expenses is None:
            return jsonify({'success': False, 'message': 'Error calculating total expenses for the trip.'})

        if total_expenses > budget:
            return jsonify({'success': False, 'message': 'Insufficient budget for the selected destination.'})

        # If budget is sufficient, proceed with retrieving travel planning details
        # Fetch day-wise travel details based on budget
        travel_plan = []
        total_expense = 0
        current_date = from_date
        with mysql.connection.cursor() as cur:
            while current_date <= to_date and total_expense < budget:
                # Fetch day-wise details and expense for the current date from the database
                cur.execute("SELECT day, description, expense FROM daywise_travel_details WHERE destination_id = %s AND date = %s",
                            (selected_destination, current_date))
                day_details = cur.fetchone()

                if day_details:
                    day = day_details['day']
                    description = day_details['description']
                    expense = day_details['expense']

                    # Check if adding the expense exceeds the budget
                    if total_expense + expense <= budget:
                        total_expense += expense
                        day_plan = {
                            'date': current_date.strftime('%d/%m/%Y'),
                            'day': day,
                            'description': description,
                            'expense': expense
                        }
                        travel_plan.append(day_plan)

                # Move to the next day
                current_date += timedelta(days=1)

        if not travel_plan:
            return jsonify({'success': False, 'message': 'No travel planning found within the budget.'})

        return jsonify({'success': True, 'message': 'Travel planning retrieved successfully.', 'travel_plan': travel_plan})

    except Exception as e:
        print(f"Error retrieving travel planning: {e}")
        return jsonify({'success': False, 'message': f'Error retrieving travel planning: {e}'})


@app.route('/get_budget_options', methods=['GET'])
def get_budget_options():
    try:
        # Extract selected destination from the request
        selected_destination = request.args.get('selectedDestination')

        # Connect to MySQL database (Assuming you've already configured the MySQL connection)

        # Execute SQL query to fetch budget options for the selected destination
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT id, amount FROM budgets WHERE destination_id = %s", (selected_destination,))
            budgets = cursor.fetchall()

        # Prepare response data
        response_data = {'budgets': [{'id': budget[0], 'amount': budget[1]} for budget in budgets]}
        return jsonify(response_data)

    except Exception as e:
        # Handle errors
        return jsonify({'error': 'Failed to fetch budget options. Please try again later.'}), 500


@app.route('/fetch-budget', methods=['POST'])
def fetch_budget():
    try:
        # Get the selected destination, from date, and to date from the AJAX request
        selected_destination = request.json.get('selectedDestination')
        from_date = request.json.get('fromDate')
        to_date = request.json.get('toDate')

        # Execute SQL query to fetch budget details from the database
        with mysql.connection.cursor() as cursor:
            cursor.execute("""
                SELECT budget_amount 
                FROM user_budgets 
                WHERE destination_id = %s 
                    AND start_date <= %s 
                    AND end_date >= %s
                """, (selected_destination, from_date, to_date))
            budget_row = cursor.fetchone()

        if budget_row:
            budget_amount = budget_row[0]
            return jsonify({'success': True, 'budget': budget_amount})
        else:
            return jsonify({'success': False, 'message': 'Budget details not found for the selected destination.'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/get_destinations', methods=['GET'])
def fetchDestinations():
    try:
        cur = mysql.connection.cursor(cursorclass=cursors.DictCursor)
        cur.execute("SELECT * FROM destinations")
        destinations = cur.fetchall()
        cur.close()

        # Convert the results to a list of dictionaries
        destinations_list = []
        for destination in destinations:
            destination_dict = {
                'id': destination['id'],
                'name': destination['name'],
                'description': destination['description'],
                # Add more fields as needed
            }
            destinations_list.append(destination_dict)

        return jsonify({'destinations': destinations_list})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/get_daywise_travel_details', methods=['POST'])
def get_daywise_travel_details():
    try:
        selected_destination = request.json.get('destination')
        from_date_str = request.json.get('fromDate')
        to_date_str = request.json.get('toDate')
        budget = float(request.json.get('budget'))  # Convert budget to float

        # Validate date values
        if not all([selected_destination, from_date_str, to_date_str, budget]):
            return jsonify({'success': False, 'message': 'Invalid input. Please provide all required parameters.'})

        # Validate and parse date strings
        try:
            from_date = parse(from_date_str)
            to_date = parse(to_date_str)
        except ValueError:
            return jsonify({'success': False, 'message': 'Invalid date format. Please provide valid date strings.'})

        # Fetch day-wise travel details based on destination, date range, and budget
        with mysql.connection.cursor(cursorclass=cursors.DictCursor) as cur:
            cur.execute(
                f"SELECT day, description FROM daywise_travel_details WHERE destination_id = {selected_destination} AND date BETWEEN '{from_date_str}' AND '{to_date_str}'")
            daywise_details = cur.fetchall()

        if not daywise_details:
            return jsonify({'success': True, 'message': 'No day-wise travel details found.', 'daywise_details': []})

        # Filter day-wise details based on budget
        filtered_daywise_details = [day for day in daywise_details if day['budget'] <= budget]

        if not filtered_daywise_details:
            return jsonify({'success': True, 'message': 'No day-wise travel details found within the provided budget.', 'daywise_details': []})

        # Format day-wise details
        formatted_daywise_details = [f'Day {day["day"]}: {day["description"]}' for day in filtered_daywise_details]

        return jsonify({'success': True, 'message': 'Day-wise travel details found.',
                        'daywise_details': formatted_daywise_details})

    except Exception as e:
        print(f"Error retrieving day-wise travel details: {e}")
        return jsonify({'success': False, 'message': f'Error retrieving day-wise travel details: {e}'})


@app.route('/')
def payment_page():
    return render_template('payment.html')


@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Retrieve user details and destination details
    username = request.form['username']
    destination = request.form['destination']
    amount = calculate_total_amount()  # Implement your logic to calculate the total amount

    # Generate PDF and send email (not implemented in this example)

    return f"Payment processed successfully! Amount: {amount}"


def calculate_total_amount():
    # Implement your logic to calculate the total amount based on destination, user details, etc.
    return 1000  # Replace with your actual calculation


@app.route('/payment', methods=['GET'])
def payment():
    username = request.args.get('username')
    user_email = request.args.get('user_email')
    destination_name = request.args.get('destination_name')
    budget = request.args.get('budget')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    total_amount = request.args.get('total_amount')

    # You can perform additional logic here if needed

    return render_template('payment.html', username=username, user_email=user_email, destination_name=destination_name,
                           budget=budget, from_date=from_date, to_date=to_date, total_amount=total_amount)


@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    # Extract user and destination details from the request
    user_details = request.json.get('user')
    destination_details = request.json.get('destination')
    total_amount = request.json.get('total_amount')

    # Generate HTML content for the PDF
    html_content = render_template('pdf_template.html', user=user_details, destination=destination_details,
                                   total_amount=total_amount)

    # Save HTML content to a temporary file
    with open('temp.html', 'w') as f:
        f.write(html_content)


def get_chatbot_response(user_message):
    try:
        # Create a cursor object to execute SQL queries using the flask_mysqldb extension
        cursor = mysql.connection.cursor()

        # Execute a query to fetch the response based on the user's message
        query = "SELECT response FROM chatbot_responses WHERE user_message = %s"
        cursor.execute(query, (user_message.lower(),))

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor (Note: Connection is managed by Flask, so no need to close it explicitly)

        # Check if a response was found in the database
        if result:
            return result[0]
        else:
            # If no response is found, provide a default response
            return 'I did not understand that. Can you please rephrase?'

    except Exception as e:
        # Handle any database connection or query errors
        return f"An error occurred: {str(e)}"


# Route to handle incoming chat messages
@app.route('/process-message', methods=['POST'])
def process_message():
    try:
        # Get the user's message from the request
        user_message = request.json.get('message')

        # Fetch the chatbot response based on user's message
        response = get_chatbot_response(user_message)

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': str(e)})

# Modify the route to fetch package details
@app.route('/get_package_details', methods=['GET'])
def get_package_details():
    try:
        # Fetch package details from the database
        # Assuming you have a table named 'packages' with columns: id, name, ratings, price, location, days, person
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM packages")
            packages = cur.fetchall()

        # Convert the fetched data to a list of dictionaries
        package_details = [{'id': package['id'],
                            'name': package['name'],
                            'ratings': package['ratings'],
                            'price': package['price'],
                            'location': package['location'],
                            'days': package['days'],
                            'person': package['person']} for package in packages]

        return jsonify({'success': True, 'packages': package_details})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_available_packages', methods=['POST'])
def get_available_packages():
    try:
        # Get selected destination and date range from the request
        selected_destination = request.json.get('selected_destination')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')

        # Query the database to fetch available packages for the selected destination and date range
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM packages WHERE destination=%s AND start_date >= %s AND end_date <= %s",
                       (selected_destination, start_date, end_date))
        available_packages = cursor.fetchall()

        return jsonify({'success': True, 'packages': available_packages})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/book_package', methods=['POST'])
def book_package():
    try:
        # Get package ID from the request
        package_id = request.json.get('package_id')

        # Implement your booking logic here

        return jsonify({'success': True, 'message': 'Booking successful!'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
