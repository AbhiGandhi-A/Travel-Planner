import smtplib
import traceback

import requests
from flask import jsonify, request
import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import random
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import mysql.connector
from flask import Flask, request, jsonify, session
from datetime import datetime
from flask import Flask, jsonify, render_template, session
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from flask import Flask, request, jsonify
from datetime import datetime
from datetime import datetime, timedelta
from dateutil.parser import parse
from flask import Flask, request, render_template
import json
from flask import Flask, session
import random
import mysql.connector
import mysql.connector
import datetime
import mysql.connector
from datetime import datetime
import mysql.connector
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_mysqldb import MySQLdb, cursors
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from flask_mysqldb import MySQL
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import traceback
from mysql.connector import cursor

app = Flask(__name__, static_url_path='/static')
CORS(app)
app = Flask(__name__)
app.secret_key = 'abhi'

# MySQL Config
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user'


mysql = MySQL(app)

# Update your database configuration here
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'user',  # Replace with your actual database name
    'port': 3306,
    'cursorclass': cursors.DictCursor
}

# Flask-Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] =   # Update with your Gmail email
app.config['MAIL_PASSWORD'] =   # Update with your generated app password


app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace 'smtp.example.com' with your SMTP server address
app.config['MAIL_PORT'] = 587  # Replace 587 with your SMTP server port number (usually 587 for TLS)
app.config['MAIL_USE_TLS'] = True  # Set to True if your SMTP server requires TLS encryption
app.config['MAIL_USE_SSL'] = False  # Set to True if your SMTP server requires SSL encryption
app.config['MAIL_USERNAME'] =  # Replace with your email address
app.config['MAIL_PASSWORD'] = 

mail = Mail(app)



# Generate a random 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))


@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/get_carousel_data', methods=['GET'])
def get_carousel_data():
    try:
        # Fetch carousel data from the database
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT image_url, caption FROM carousel_items")  # Use correct column names
            carousel_items = cur.fetchall()

        # Convert the fetched data to a list of dictionaries
        carousel_data = [{'image': item[0], 'caption': item[1]} for item in carousel_items]

        return jsonify({'success': True, 'carousel_data': carousel_data})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


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

        # Query the database to retrieve user information
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()

        if user:
            user_id = user[0]  # Accessing the first element of the tuple (ID)
            username = user[1]  # Accessing the second element of the tuple (username)

            # Update login status in the database
            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE users SET login_status = %s WHERE id = %s", ('logged_in', user_id))
                mysql.connection.commit()

            # Store user ID in session
            session['user_id'] = user_id

            return jsonify({'success': True, 'message': 'Login successful', 'username': username})

        else:
            return jsonify({'success': False, 'error': 'Invalid username or password'})

    except Exception as e:
        # Handle any unexpected errors
        return jsonify({'success': False, 'error': str(e)})





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



@app.route('/get_package_details', methods=['GET'])
def get_package_details():
    try:
        # Fetch package details from the database
        with mysql.connection.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM packages")
            packages = cur.fetchall()

        # Convert the fetched data to a list of dictionaries
        package_details = [{'id': package['id'],
                            'destination_id': package['destination_id'],
                            'hotel': package['hotel'],
                            'place': package['place'],
                            'budget': float(package['budget']),  # Convert Decimal to float
                            'guest': package['guest'],
                            'image_url': package['image_url'],
                            'start_date': str(package['start_date']),  # Convert date object to string
                            'end_date': str(package['end_date'])} for package in packages]

        return jsonify({'success': True, 'packages': package_details})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_budget_options', methods=['GET'])
def get_budget_options():
    try:
        # Extract selected destination from the request
        selected_destination = request.args.get('selectedDestination')

        # Connect to MySQL database (Assuming you've already configured the MySQL connection)

        # Execute SQL query to fetch budget options for the selected destination
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT id, amount, price_per_person FROM budgets WHERE destination_id = %s",
                           (selected_destination,))
            budgets = cursor.fetchall()

        # Prepare response data
        response_data = {
            'budgets': [{'id': budget[0], 'amount': budget[1], 'price_per_person': budget[2]} for budget in budgets]}
        return jsonify(response_data)

    except Exception as e:
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
        cursor.close()

        # Check if a response was found in the database
        if result:
            return result[0]
        else:
            # If no response is found, provide a default response
            return 'I did not understand that. Can you please rephrase?'

    except Exception as e:
        # Handle any database connection or query errors
        return f"An error occurred: {str(e)}"

@app.route('/packages')  # Define the correct URL pattern for displaying packages
def display_packages():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM packages")
        packages = cur.fetchall()
        cur.close()
        return render_template('package.html', packages=packages)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/check_login_status')
def check_login_status():
    # Here you would implement logic to check the user's login status
    # Assuming you have the user's information available in the session
    if 'user_id' in session:
        # User is logged in
        return jsonify({'logged_in': True})
    else:
        # User is not logged in
        return jsonify({'logged_in': False})

@app.route('/get_available_packages', methods=['POST'])
def get_available_packages():
    try:
        selected_destination = request.json.get('selected_destination')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')

        cursor = mysql.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM packages WHERE destination_id = %s AND start_date >= %s AND end_date <= %s",
                       (selected_destination, start_date, end_date))
        available_packages = cursor.fetchall()

        return jsonify({'success': True, 'packages': available_packages})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# Route to handle the booking form submission
# Modify the submit_booking route to save the booking details to the database
# Modify the submit_booking route to save the booking details to the database
# Endpoint to fetch booking details based on package ID
@app.route('/fetch_booking_details', methods=['GET'])
def fetch_booking_details():
    try:
        package_id = request.args.get('packageId')

        # Fetch booking details based on the package ID from the database
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM bookings WHERE package_id = %s", (package_id,))
            booking_details = cur.fetchall()

        return jsonify({'success': True, 'bookingDetails': booking_details})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})




@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    try:
        # Check if the user is logged in
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'User ID not found. Please log in to proceed with booking.'})

        # Get the user ID from the session
        user_id = session['user_id']

        # Get booking details from the request JSON
        data = request.json
        package_id = data.get('packageId')
        start_date_str = data.get('startDate')  # Assuming dates are sent as strings
        end_date_str = data.get('endDate')

        # Ensure all required fields are present
        if not package_id or not start_date_str or not end_date_str:
            return jsonify({'success': False, 'error': 'Incomplete booking details'})

        # Convert start_date and end_date strings to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # Insert booking details into the database
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO bookings (user_id, package_id, start_date, end_date) VALUES (%s, %s, %s, %s)",
                        (user_id, package_id, start_date, end_date))
            mysql.connection.commit()

        # Fetch package details for the booked package

        # Send confirmation email to the user
        send_booking_confirmation_email(user_id)

        # Send package details email to the user

        return jsonify({'success': True, 'message': 'Booking successful'})

    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error in submit_booking route: {str(e)}")
        return jsonify({'success': False, 'error': 'An error occurred while processing the booking. Please try again later.'})

def fetch_package_details(package_id):
    try:
        # Fetch package details from the database based on package_id
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM packages WHERE id = %s", (package_id,))
            package_details = cur.fetchone()

        if package_details:
            return {
                'id': package_details[0],
                'destination_id': package_details[1],
                'hotel': package_details[2],
                'place': package_details[3],
                'budget': float(package_details[4]),  # Assuming 'budget' is a decimal type
                'guest': package_details[5],
                'image_url': package_details[6],
                'start_date': str(package_details[7]),  # Convert date objects to strings
                'end_date': str(package_details[8])
            }
        else:
            return None

    except Exception as e:
        print("Error fetching package details:", e)
        return None

def send_booking_confirmation_email(user_id):
    try:
        user_email = get_user_email(user_id)

        if user_email:
            sender_email = app.config['MAIL_USERNAME']
            subject = "Booking Confirmation"
            body = "Your booking has been confirmed. Thank you for choosing our service!"

            msg = MIMEMultipart()
            msg.attach(MIMEText(body, 'plain'))
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = user_email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, app.config['MAIL_PASSWORD'])
                server.sendmail(sender_email, user_email, msg.as_string())

            print("Confirmation email sent successfully to:", user_email)
        else:
            print("User email not found for user ID:", user_id)

    except Exception as e:
        print("Error sending confirmation email:", e)


def send_package_details_email(user_id, package_details):
    try:
        user_email = get_user_email(user_id)

        if user_email and package_details:
            sender_email = app.config['MAIL_USERNAME']
            subject = "Your Booked Package Details"
            body = f"Thank you for booking with us! Here are the details of your booked package:\n\n" \
                   f"Destination: {package_details['place']}\n" \
                   f"Hotel: {package_details['hotel']}\n" \
                   f"Budget: {package_details['budget']}\n" \
                   f"Start Date: {package_details['start_date']}\n" \
                   f"End Date: {package_details['end_date']}\n\n" \
                   f"We hope you have a wonderful trip!"

            msg = MIMEMultipart()
            msg.attach(MIMEText(body, 'plain'))
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = user_email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, app.config['MAIL_PASSWORD'])
                server.sendmail(sender_email, user_email, msg.as_string())

            print("Package details email sent successfully to:", user_email)
            return jsonify({'success': True, 'message': 'Package details email sent successfully'})
        else:
            if not user_email:
                print("User email not found for user ID:", user_id)
            if not package_details:
                print("Package details not found for user ID:", user_id)

            # Return an error response
            return jsonify({'success': False, 'error': 'Package details email could not be sent'})

    except Exception as e:
        print("Error sending package details email:", e)
        return jsonify({'success': False, 'error': str(e)})


def get_user_email(user_id):
    try:
        # Retrieve user's email from the database based on user ID
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT email FROM users WHERE id = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                return user_data[0]  # Assuming email is stored in the first column
            else:
                return None

    except Exception as e:
        print("Error retrieving user email:", e)
        return None

from decimal import Decimal  # Import Decimal from decimal module

@app.route('/show_travel_plan', methods=['POST'])
def show_travel_plan():
    try:
        user_id = session.get('user_id')  # Assuming user_id is stored in the session
        if not user_id:
            return jsonify({'success': False, 'error': 'User ID not found'})

        selected_destination = request.json['selected_destination']
        from_date = request.json['from_date']
        to_date = request.json['to_date']
        selected_adults = int(request.json.get('adults', 0))  # Get adults if provided, default to 0
        selected_children = int(request.json.get('children', 0))  # Get children if provided, default to 0

        # Fetch packages available for the selected destination and dates
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT id, destination_id, hotel, place, budget, guest, image_url, start_date, end_date, adult_price, child_price
            FROM packages 
            WHERE destination_id = %s AND start_date >= %s AND end_date <= %s
        """, (selected_destination, from_date, to_date))
        packages = cursor.fetchall()

        # Fetch budget data to calculate total budget
        cursor.execute("SELECT amount FROM budgets WHERE destination_id = %s",
                       (selected_destination,))
        budget_data = cursor.fetchone()

        # Convert fetched data to a list of dictionaries for JSON response
        package_list = []
        total_guests = 0  # Initialize total_guests
        total_budget = 0  # Initialize total_budget

        for package in packages:
            package_dict = {
                'id': package[0],
                'destination_id': package[1],
                'hotel': package[2],
                'place': package[3],
                'budget': float(package[4]),  # Assuming 'budget' is a decimal type
                'guest': package[5],
                'image_url': package[6],
                'start_date': str(package[7]),  # Convert date objects to strings
                'end_date': str(package[8]),
                'adult_price': float(package[9]),  # Convert Decimal to float
                'child_price': float(package[10])  # Convert Decimal to float
            }
            package_list.append(package_dict)

            total_budget += float(selected_adults) * package_dict['adult_price']  # Convert selected_adults to float
            total_budget += float(selected_children) * package_dict['child_price']  # Convert selected_children to float
            total_guests += selected_adults + selected_children

        if budget_data:
            total_budget += float(budget_data[0])  # Convert budget_data[0] to float

            with mysql.connection.cursor() as cur:
                cur.execute("UPDATE users SET total_budget = %s, total_guests = %s WHERE id = %s",
                            (total_budget, total_guests, user_id))
                mysql.connection.commit()

            return jsonify({
                'success': True,
                'total_budget': total_budget,
                'total_guests': total_guests if total_guests > 0 else None,  # Return None if no guests selected
                'packages': package_list,
            })
        else:
            return jsonify({'success': False, 'error': 'Budget details not found'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_packages', methods=['GET'])
def get_packages(db_cursor=None):
    try:
        db_cursor.execute("SELECT * FROM your_package_table")
        packages = db_cursor.fetchall()
        return jsonify({'packages': packages})

    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/save_booking', methods=['POST'])
def save_booking():
    try:
        package_id = request.json.get('packageId')
        print("Received booking request for package ID:", package_id)

        # Process the booking request

        return jsonify({'success': True, 'message': 'Booking successful'})
    except Exception as e:
        print("Error occurred while processing booking:", e)
        return jsonify({'success': False, 'error': str(e)})

@app.route('/logout', methods=['POST'])
def logout():
    try:
        # Get user's username from session or request data
        user_id = session.get('user_id')

        # Update the user's login status to 'logged_out' in the database
        with mysql.connection.cursor() as cur:
            cur.execute("UPDATE users SET login_status = %s WHERE id = %s", ('logged_out', user_id))
            mysql.connection.commit()

        # Clear the session data
        session.clear()

        return jsonify({'success': True, 'message': 'Logout successful'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def get_database_connection():
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connection
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None


# Modify the book_package route to handle the booking request properly
@app.route('/book_package', methods=['POST'])
def book_package():
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'User not logged in'})

        # Parse data from the request
        data = request.json
        package_id = data.get('package_id')
        user_id = session['user_id']
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Validate data (e.g., check if required fields are present)

        # Connect to the database
        connection = mysql.connection
        cursor = connection.cursor()

        # Insert booking into the database
        cursor.execute("INSERT INTO bookings (user_id, package_id, start_date, end_date, booking_date ) VALUES (%s, %s, %s, %s, %s)",
                       (user_id, package_id, start_date, end_date, datetime.now()))

        # Commit changes
        connection.commit()

        # Close connection
        cursor.close()

        # Send email notification to the user
        send_booking_confirmation_email(user_id)

        return jsonify({'success': True, 'message': 'Booking successful'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



@app.route('/fetch_bookings', methods=['GET'])
def fetch_bookings():
    try:
        # Retrieve user ID from the session
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({'success': False, 'error': 'User not logged in'})

        # Query the database to fetch bookings for the user
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM bookings WHERE user_id = %s", (user_id,))
        user_bookings = cursor.fetchall()
        cursor.close()

        if user_bookings is not None and user_bookings:
            # Convert the bookings to a list of dictionaries
            bookings_list = []
            for booking in user_bookings:
                booking_dict = {
                    'id': booking[0],
                    'user_id': booking[1],
                    'package_id': booking[2],
                    'start_date': booking[3].strftime('%Y-%m-%d') if booking[3] else None,
                    'end_date': booking[4].strftime('%Y-%m-%d') if booking[4] else None,
                    'booking_date': booking[5].strftime('%Y-%m-%d %H:%M:%S') if booking[5] else None,
                    'booking_status': booking[6],
                }
                bookings_list.append(booking_dict)

            return jsonify({'success': True, 'bookings': bookings_list})
        else:
            return jsonify({'success': True, 'bookings': []})  # Return empty bookings list if no bookings found

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    try:
        # Retrieve booking ID from the request
        booking_id = request.form['booking_id']

        # Perform the cancellation in the database
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Booking successfully cancelled!'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# Flask route to fetch tour packages from the database
from flask import jsonify

@app.route('/fetch_packages', methods=['GET'])
def fetch_packages():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tour_packages")
        packages = cursor.fetchall()
        cursor.close()

        # Format the data before returning the JSON response
        formatted_packages = []
        for package in packages:
            formatted_package = {
                'id': package[0],
                'location': package[1],
                'image_url': package[2],
                'days': package[3],
                'ratings': float(package[4]),  # Convert decimal to float
                'price': float(package[5]),    # Convert decimal to float
                'guest_count': package[6]
            }
            formatted_packages.append(formatted_package)

        return jsonify({'packages': formatted_packages})

    except Exception as e:
        return jsonify({'error': str(e)})

# Flask route to book a tour package
@app.route('/book_tour_package', methods=['POST'])
def book_tour_package():
    try:
        data = request.json
        package_id = data.get('package_id')
        guest_count = data.get('guest_count')

        if 'user_id' not in session:
            # Redirect to the login page if the user is not logged in
            return jsonify({'success': False, 'error': 'User not logged in'})

        # Get the user ID from the session
        user_id = session['user_id']

        # Insert booking details into the database
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO bookings (user_id, package_id, guest_count, booked_by) VALUES (%s, %s, %s, %s)",
                        (user_id, package_id, guest_count, user_id))
            mysql.connection.commit()

        # Send booking confirmation email to the user
        send_booking_confirmation_email(user_id)

        return jsonify({'success': True, 'message': 'Booking successful'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Your other Flask routes and functions

def generate_transaction_id():
    # Generate a unique transaction ID using a combination of timestamp and a random number
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_number = random.randint(1000, 9999)  # Example random number range
    transaction_id = f'TRANS{timestamp}{random_number}'
    return transaction_id


def get_database_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
        return None

# Modify the save_payment_details function to include package_id as a parameter
def save_payment_details(cardNumber, expiryDate, cvv, transactionId, package_id, startDate, endDate, user_id):
    try:
        connection = mysql.connection  # Access MySQL connection from Flask's MySQL extension
        if connection:
            cursor = connection.cursor()

            cursor.execute("INSERT INTO payment_status (package_id, payment_status, transaction_id, payment_date, user_id) VALUES (%s, 'success', %s, NOW(), %s)",
                           (package_id, transactionId, user_id))  # Save package ID and user ID
            connection.commit()

            cursor.close()
        else:
            raise Exception("Database connection not available")
    except Exception as e:
        print("Error saving payment details:", e)

def fetch_user_total_budget(user_id):
    try:
        # Assuming you are using a database connection called `mysql` and a cursor object
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT total_budget FROM users WHERE id = %s", (user_id,))
        total_budget = cursor.fetchone()
        cursor.close()
        return total_budget[0] if total_budget else None
    except Exception as e:
        print("Error fetching user total budget:", e)
        return None


def send_payment_confirmation_email(transactionId, user_id, package_id):
    try:
        user_email = get_user_email(user_id)
        sender_email = app.config['MAIL_USERNAME']
        subject = "Payment Confirmation"

        # Fetch package details for the booked package
        package_details = fetch_package_details(package_id)

        # Fetch total budget from the users table
        total_budget = fetch_user_total_budget(user_id)

        body = f"""
            <html>
            <head>
                <style>
                    .email-body {{
                        font-family: Arial, sans-serif;
                        font-size: 14px;
                        line-height: 1.8;
                    }}
                    .package-details {{
                        margin-top: 20px;
                        padding: 10px;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        background-color: #f9f9f9;
                    }}
                    .package-label {{
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body class="email-body">
                <div class="package-details">
                    <p>Your payment with transaction ID {transactionId} has been successfully processed.</p>
                    <p class="package-label">Package Details:</p>
                    <p><b>Destination:</b> {package_details['place']}</p>
                    <p><b>Hotel:</b> {package_details['hotel']}</p>
                    <p><b>Total Budget:</b> {total_budget}</p>  
                    <p><b>Start Date:</b> {package_details['start_date']}</p>
                    <p><b>End Date:</b> {package_details['end_date']}</p>
                    <img src="{package_details['image_url']}" alt="Package Image">
                </div>
            </body>
            </html>
        """

        msg = Message(subject, sender=sender_email, recipients=[user_email])
        msg.body = body
        msg.html = body  # Set the HTML content of the email

        mail.send(msg)

        print("Payment confirmation email sent successfully to:", user_email)
    except Exception as e:
        print("Error sending payment confirmation email:", e)
        return jsonify({'success': False, 'error': str(e)})


@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        # Retrieve payment details and package details from the request JSON
        data = request.json
        cardNumber = data.get('cardNumber')
        expiryDate = data.get('expiryDate')
        cvv = data.get('cvv')
        package_id = data.get('packageId')  # Ensure 'package_id' is correctly defined
        startDate = data.get('startDate')
        endDate = data.get('endDate')
        user_id = session['user_id']  # Get the user ID from the session

        # Validate payment details and other necessary data
        if not cardNumber or not expiryDate or not cvv or not package_id or not startDate or not endDate:
            return jsonify({'success': False, 'error': 'Incomplete payment details'})

        # Generate a unique transaction ID
        transactionId = generate_transaction_id()  # Using the function you provided

        # Save payment details and update payment status in the database
        save_payment_details(cardNumber, expiryDate, cvv, transactionId, package_id, startDate, endDate, user_id)

        # Send email with transaction ID to the user
        send_payment_confirmation_email(transactionId, user_id, package_id)  # Pass the package_id parameter

        return jsonify({'success': True, 'message': 'Payment successful'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/update_payment_status', methods=['POST'])
def update_payment_status():
    try:
        data = request.json
        package_id = data.get('packageId')
        status = data.get('status')

        # Perform the update operation in the payment_status table
        with mysql.connection.cursor() as cur:
            cur.execute("INSERT INTO payment_status (package_id, payment_status, payment_date) VALUES (%s, %s, NOW()) "
                        "ON DUPLICATE KEY UPDATE payment_status = VALUES(payment_status), payment_date = NOW()",
                        (package_id, status))
            mysql.connection.commit()

        return jsonify({'success': True, 'message': 'Payment status updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/fetch_transaction_id', methods=['POST'])
def fetch_transaction_id():
    try:
        data = request.json
        payment_id = data.get('payment_id')

        if not payment_id:
            raise ValueError('Payment ID is missing in the request')

        # Fetch transaction ID from payment_status table using payment ID
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT transaction_id FROM payment_status WHERE id = %s", (payment_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return jsonify({'success': True, 'transaction_id': result[0]})
        else:
            return jsonify({'success': False, 'error': 'Transaction ID not found'})

    except ValueError as ve:
        return jsonify({'success': False, 'error': str(ve)})
    except mysql.connector.Error as e:
        return jsonify({'success': False, 'error': f"MySQL Error: {str(e)}"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/process_refund', methods=['POST'])
def process_refund():
    try:
        data = request.json
        app.logger.info(f"Received refund request data: {data}")

        transaction_id = data.get('transaction_id')
        bank_account = data.get('bank_account')

        # Perform refund process and store refund details in the database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO refund_status (transaction_id, bank_account, status) VALUES (%s, %s, 'pending')",
                       (transaction_id, bank_account))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Refund requested successfully'})
    except Exception as e:
        print("Error processing refund:", e)  # Log the error for debugging
        return jsonify({'success': False, 'error': str(e)})



    @app.route('/fetch_bank_name', methods=['POST'])
    def fetch_bank_name():
        try:
            data = request.json
            ifsc_code = data.get('ifsc_code')

            # Fetch bank name based on IFSC code from the database
            cursor = mysql.cursor(dictionary=True)
            cursor.execute("SELECT bank_name FROM refund_status WHERE ifsc_code = %s", (ifsc_code,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                return jsonify({'success': True, 'bank_name': result['bank_name']})
            else:
                return jsonify({'success': False, 'error': 'Bank name not found'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

@app.route('/retry_payment', methods=['POST'])
def retry_payment():
    try:
        data = request.json
        transaction_id = data.get('transaction_id')

        # Update payment_status to 'success' for retry
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE payment_status SET payment_status = 'success' WHERE transaction_id = %s",
                       (transaction_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Payment retried successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})



@app.route('/get_user_payments', methods=['GET'])
def get_user_payments():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'User not logged in'})

        # Get MySQL cursor
        cursor = mysql.connection.cursor()

        # Fetch payments for the logged-in user including payment ID, package ID, and payment date
        cursor.execute("SELECT id, transaction_id, payment_status, payment_date, package_id FROM payment_status WHERE user_id = %s",
                       (user_id,))
        payments = cursor.fetchall()

        # Convert the fetched data to a list of dictionaries for JSON response
        payment_list = [{'id': payment[0], 'transaction_id': payment[1], 'payment_status': payment[2], 'payment_date': payment[3], 'package_id': payment[4]} for payment in payments]

        # Close cursor after fetching data
        cursor.close()

        return jsonify({'success': True, 'payments': payment_list})
    except Exception as e:
        print("Error in get_user_payments:", e)  # Log the error for debugging
        return jsonify({'success': False, 'error': 'An error occurred while fetching payments'})


# Python Flask routes for data retrieval
# Route to fetch top destinations with image URLs
@app.route('/fetch_top_destinations_with_images', methods=['GET'])
def fetch_top_destinations_with_images():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, destination_name, image_url FROM top_destinations")
        top_destinations = cursor.fetchall()
        cursor.close()

        formatted_destinations = [{'id': dest[0], 'name': dest[1], 'image_url': dest[2]} for dest in top_destinations]

        return jsonify({'top_destinations': formatted_destinations})

    except Exception as e:
        return jsonify({'error': str(e)})

# Route to fetch destination lists for a top destination
@app.route('/fetch_destination_list', methods=['GET'])
def fetch_destination_list():
    try:
        top_destination_id = request.args.get('top_destination_id')

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM destination_lists WHERE top_destination_id = %s", (top_destination_id,))
        destination_list = cursor.fetchall()
        cursor.close()

        formatted_list = [{'id': dest[0], 'name': dest[2]} for dest in destination_list]

        return jsonify({'destination_list': formatted_list})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/about/data')
def about_data():
    # Replace these placeholders with actual data retrieval logic
    data = {
        'about': 'we aim to provide a brief overview of the platform s mission and vision. Our goal is to revolutionize the way people plan and experience travel by offering personalized and hassle-free travel packages. With a focus on user satisfaction, convenience, and innovative technology integration, we strive to make travel planning an enjoyable and memorable experience for all our users.',
    }
    return jsonify(data)


@app.route('/contact/data')
def contact_data():
    # Replace these placeholders with actual contact information
    data = {
        'email': 'example@example.com',
        'phone': '123-456-7890',
        'address': '123 Street, City, Country'
    }
    return jsonify(data)

@app.route('/get_airplane_options', methods=['GET'])
def get_airplane_options():
    try:
        # Connect to MySQL database (Assuming you've already configured the MySQL connection)

        # Execute SQL query to fetch airplane options from the database
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT id, name, price, departure_time FROM airplanes")
            airplanes = cursor.fetchall()

        # Prepare response data
        response_data = {
            'airplanes': [{'id': airplane[0], 'name': airplane[1], 'price': airplane[2], 'departure_time': airplane[3]} for airplane in airplanes]}
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': 'Failed to fetch airplane options. Please try again later.'}), 500

from flask import render_template, redirect, url_for

@app.route('/bookings')
def bookings():
    # Check if the user is logged in
    if 'user_id' in session:
        # Render the bookings page for the logged-in user
        return render_template('bookings.html')
    else:
        # Redirect to the login page if the user is not logged in
        return redirect('/login')  # Assuming you have a login route

@app.route('/payments')
def payments():
    # Check if the user is logged in
    if 'user_id' in session:
        # Render the payments page for the logged-in user
        return render_template('payments.html')
    else:
        # Redirect to the login page if the user is not logged in
        return redirect('/login')  # Assuming you have a login route


if __name__ == '__main__':
    app.run(debug=True, port=5000)
