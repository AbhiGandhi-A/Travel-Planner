document.addEventListener('DOMContentLoaded', function () {

    // Function to show travel plan details
    document.getElementById('showMessageButton').addEventListener('click', function () {
        document.getElementById('loadingAnimation').style.display = 'block';
        setTimeout(function () {
            // Hide loading animation after some delay (simulating server response time)
            document.getElementById('loadingAnimation').style.display = 'none';



        const packageDetails = document.getElementById('packageDetails');
        packageDetails.innerHTML = '';
        const selectedDestination = document.getElementById('destinationSelect').value;
        const fromDate = document.getElementById('fromDateInput').value;
        const toDate = document.getElementById('toDateInput').value;
        const selectedAdults = document.getElementById('adultSelect').value;
        const selectedChildren = document.getElementById('childSelect').value;
        const userId = sessionStorage.getItem('user_id'); // Assuming user_id is stored in sessionStorage
    
        fetch('/show_travel_plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId, // Pass the user_id as part of the request
                selected_destination: selectedDestination,
                from_date: fromDate,
                to_date: toDate,
                adults: selectedAdults,
                children: selectedChildren
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Process the received data and display package details
            if (data.success) {
                const totalBudget = data.total_budget;
                const totalGuests = data.total_guests;

                // Update the UI with total budget and total guests
                document.getElementById('totalBudget').value = '' + totalBudget;
                document.getElementById('totalGuests').value = '' + totalGuests;

                // Display package details (assuming package data is available in 'data.packages')
                if (data.packages && data.packages.length > 0) {
                    data.packages.forEach(package => {
                        // Assuming 'package' is an object containing package details
                        const packageHtml = `
                            <div class="package">
                                <h3>${package.hotel}</h3>
                                <p>Location: ${package.place}</p>
                                <p>Package Guest: ${package.guest}</p>
                                <p>Total Guests: ${totalGuests+package.guest}</p>
                                <p>Budget of Package: ${package.budget}</p>
                                <p>Total Budget: ${totalBudget}</p>
                                <img src="${package.image_url}" alt="Package Image">
                                <button class="btn btn-primary book-now-btn" data-package-id="${package.id}">Book Now</button>
                            </div>
                        `;
                        document.getElementById('packageDetails').innerHTML += packageHtml;
                    });


                    // Attach event listener to book now buttons
                    document.querySelectorAll('.book-now-btn').forEach(button => {
                        button.addEventListener('click', function () {
                            // Handle book now button click event

                            if (button.disabled) return; // Prevent multiple clicks

                            // Check login status before proceeding
                            fetch('/check_login_status')
                                .then(response => response.json())
                                .then(data => {
                                    if (data.logged_in) {
                                        // User is logged in, open the payment form
                                        document.getElementById('paymentModal').style.display = 'block';
                                        // Set the package ID in sessionStorage for booking process
                                        sessionStorage.setItem('package_id', button.getAttribute('data-package-id'));
                                    } else {
                                        alert("Please login to proceed");
                                        openLoginForm();
                                        window.scrollTo({ top: 0, behavior: 'smooth' });
                                        scrollToTop();
                                        // Assuming you have a function to open the login form
                                    }
                                })
                                .catch(error => console.error('Error checking login status:', error));
                        });
                    });
                } else {
                    packageDetails.innerHTML = '<p>No packages found.</p>';
                }
            } else {
                console.error('Error:', data.error);
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error: ' + error.message); // Display error in an alert box
            console.error('Error:', error);
        });
    }, 3000); 
});
    // Event listener for submitting payment form
    document.getElementById('paymentForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission behavior

        // Fetch payment details from the form
        const cardNumber = document.getElementById('cardNumber').value;
        const expiryDate = document.getElementById('expiryDate').value;
        const cvv = document.getElementById('cvv').value;
        const packageId = sessionStorage.getItem('package_id');
        const startDate = document.getElementById('fromDateInput').value;
        const endDate = document.getElementById('toDateInput').value;
        document.getElementById('paymentLoadingAnimation').style.display = 'block';

        // Make an AJAX request to process the payment
        fetch('/process_payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cardNumber: cardNumber,
                expiryDate: expiryDate,
                cvv: cvv,
                packageId: packageId,
                startDate: startDate,
                endDate: endDate
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Hide the payment loading animation after a delay (for demonstration)
            setTimeout(function () {
                document.getElementById('paymentLoadingAnimation').style.display = 'none';
            }, 2000); // Hide after 2 seconds (adjust timing as needed)
    
            // Process the payment response
            if (data.success) {
                alert('Payment successful!');
                // Continue with the booking process
                bookPackage(packageId, startDate, endDate);
                // Close the payment form
                document.getElementById('paymentModal').style.display = 'none';
            } else {
                console.error('Payment Error:', data.error);
                alert('Payment Error: ' + data.error);
            }
        })
        .catch(error => {
            alert('Error: ' + error.message); // Display error in an alert box
            console.error('Error:', error);
        });
    });

    // Event listener for "Pay Now" button
    document.getElementById('payNowButton').addEventListener('click', function () {
        const userId = sessionStorage.getItem('user_id');
        const packageId = sessionStorage.getItem('package_id');
        const startDate = document.getElementById('fromDateInput').value;
        const endDate = document.getElementById('toDateInput').value;
        bookPackage(packageId, startDate, endDate); // <-- Corrected function name
    });

    function bookPackage(packageId, startDate, endDate) {
        // Make an AJAX request to book the package
        $.ajax({
            url: '/submit_booking',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                userId: sessionStorage.getItem('user_id'), // Retrieve user ID from session
                packageId: packageId,
                startDate: startDate,
                endDate: endDate
            }),
            success: function(response) {
                if (response.success) {
                    // Booking successful
                    alert('Booking successful');
                    // Additional actions after successful booking (if any)
                } else {
                    // Booking failed
                    if (response.error) {
                        // Display error message from the server
                        alert('Booking failed: ' + response.error);
                    } else {
                        // Unexpected error
                        alert('Booking failed. Please try again later.');
                    }
                }
            },
            error: function(xhr, status, error) {
                // Error occurred during AJAX request
                console.error('Error booking package:', error);
                alert('An error occurred while processing the booking. Please try again later.');
            }
        });
    }


        // Event listener for the "Book Now" button click
        $('.book-now-btn').on('click', function() {
            const packageId = $(this).data('package-id');
            const startDate = $(this).data('start-date');
            const endDate = $(this).data('end-date');
            console.log('Book Now clicked for package ID:', packageId);

            // Call the bookPackage function to handle the booking process
            bookPackage(packageId, startDate, endDate);
        });

    });
    fetchDestinations();
    // Function to fetch destinations and update the dropdown
    // Fetch destinations from the server and populate the destination dropdown
function fetchDestinations() {
        fetch('/get_destinations')
            .then(response => response.json())
            .then(data => {
                if (data.destinations) {
                    const destinationSelect = document.getElementById('destinationSelect');
                    destinationSelect.innerHTML = ''; // Clear existing options
                    data.destinations.forEach(destination => {
                        const option = document.createElement('option');
                        option.value = destination.id;
                        option.textContent = destination.name;
                        destinationSelect.appendChild(option);
                    });
                }
            })
            .catch(error => console.error('Error fetching destinations:', error));
    }

// Fetch budget options based on the selected destination and populate the budget dropdown
function fetchBudgetOptions(selectedDestination) {
    fetch(`/get_budget_options?selectedDestination=${selectedDestination}`)
        .then(response => response.json())
        .then(data => {
            if (data.budgets) {
                const budgetSelect = document.getElementById('budgetSelect');
                budgetSelect.innerHTML = ''; // Clear existing options
                data.budgets.forEach(budget => {
                    const option = document.createElement('option');
                    option.value = budget.id;
                    option.textContent = budget.amount;
                    budgetSelect.appendChild(option);
                });
            }
        })
        .catch(error => console.error('Error fetching budget options:', error));
}

function toggleBudgetSelectVisibility(showBudgetSelect) {
    const budgetSelectSection = document.querySelector('.budget-select-section');
    if (showBudgetSelect) {
        budgetSelectSection.style.display = 'block';
    } else {
        budgetSelectSection.style.display = 'none';
    }
}



// Event listener for destination select change
document.getElementById('destinationSelect').addEventListener('change', function () {
    const selectedDestination = this.value;
    if (selectedDestination !== 'Destination') {
        fetchBudgetOptions(selectedDestination);
        toggleBudgetSelectVisibility(true); // Show budget select section
    } else {
        toggleBudgetSelectVisibility(false); // Hide budget select section
    }
});




// Event listener for the Show Travel Plan button

    // Add event listener to the Show Travel Plan button
    const showMessageButton = document.getElementById('showMessageButton');
    showMessageButton.addEventListener('click', showTravelPlan);

    // Attach the event listener to the button
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('loginLink').addEventListener('click', function () {
        openLoginForm(); // Call the function to show the login form

        document.getElementById('signup-form').addEventListener('click', function (event) {
            if (event.target.id === 'loginLink') {
                openLoginForm();
                closeOtherForms(); // Add this function
            }
        });
    });

});

 function showForm(formId) {
    $('.auth-form').hide();
    $(formId).show();
}

function closeOtherForms() {
    // Hide all forms
    $('.auth-form').hide();

    // Show only the sign-up form
    $('#signup-form').show();
}

function openLoginForm() {
    document.getElementById('signup-form').style.display = 'none';
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('forgot-password-form').style.display = 'none';
    document.getElementById('reset-password-section').style.display = 'none';
}

function openSignupForm() {
    document.getElementById('signup-form').style.display = 'block';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('forgot-password-form').style.display = 'none';
    document.getElementById('reset-password-section').style.display = 'none';
}

// Function to switch to the forgot password form

        $('#login-link').click(openLoginForm);
        $('#signup-link').click(openSignupForm);
        $('#forgot-password-link').click(openForgotPasswordForm);

        function openChatSupport() {
        $('#liveChatSupport').toggle();
        $('#openChatButton').hide(); // Hide the button once chat is open
    }

    function openChatSupport() {
        $('#liveChatSupport').toggle();
        $('#openChatButton').hide(); // Hide the button once chat is open
    }


    function toggleChatbox() {
        var chatbox = document.getElementById("liveChatSupport");
        if (chatbox.style.display === "none") {
            chatbox.style.display = "block";
        } else {
            chatbox.style.display = "none";
        }
    }

    function openChatSupport() {
    $('#liveChatSupport').fadeIn(); // Use fadeIn to show with fade effect
}

function closeChatSupport() {
    $('#liveChatSupport').fadeOut(); // Use fadeOut to hide with fade effect
}

// Other JavaScript functions (sendMessage, displayMessage) remain the same
function openChatSupport() {
    $('#liveChatSupport').show();
    $('#openChatButton').hide(); // Hide the chatbot icon button
}

function closeChatSupport() {
    $('#liveChatSupport').hide();
    $('#openChatButton').show(); // Show the chatbot icon button
}
    function sendMessage() {
        var message = $('#chatInput').val();

        if (message.trim() !== '') {
            // Assuming you have a server-side endpoint for processing messages
            $.post('/process-message', { message: message }, function (data) {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    $('#chatInput').val('');
                    $('#chatContainer').append('<div><strong>User:</strong> ' + message + '</div>');
                    $('#chatContainer').append('<div><strong>Bot:</strong> ' + data.response + '</div>');
                }
            }).fail(function () {
                alert('Error: An unexpected error occurred.');
            });
        }
    }

    // Function to send a message
    function openChatSupport() {
            $('#liveChatSupport').toggle();
            $('#openChatButton').hide(); // Hide the button once chat is open
        }

        // Function to send a message
        function sendMessage() {
    try {
        var message = $('#chatInput').val();

        if (message.trim() !== '') {
            // Assuming you have a server-side endpoint for processing messages
            $.post('/process-message', { message: message }, function (data) {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    $('#chatInput').val('');
                    $('#chatContainer').append('<div><strong>User:</strong> ' + message + '</div>');
                    $('#chatContainer').append('<div><strong>Bot:</strong> ' + data.response + '</div>');
                }
            }).fail(function () {
                alert('Error: An unexpected error occurred.');
            });
        }
    } catch (error) {
        console.error('An unexpected error occurred:', error);
        alert('Error: An unexpected error occurred.');
    }
}

var chatbot_response;  // Declare the variable outside the function

function sendMessage() {
    var userMessage = document.getElementById('chatInput').value.trim();

    if (userMessage !== '') {
        $.ajax({
            type: "POST",
            url: '/process-message',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({ message: userMessage }),
            success: function (data) {
                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    // Update the variable directly
                    chatbot_response = data.response;

                    displayMessage('User: ' + userMessage);
                    displayMessage('Chatbot: ' + chatbot_response);
                }
            },
            error: function () {
                alert('Error: An unexpected error occurred.');
            }
        });

        document.getElementById('chatInput').value = '';
    }
}

function displayMessage(message) {
    var chatContainer = document.getElementById('chatContainer');
    var messageElement = document.createElement('div');
    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
}


// Function to handle booking of a package

        document.addEventListener('DOMContentLoaded', function () {
            // Function to show a specific form
            function showForm(formId) {
                $('.auth-form').hide();
                $(formId).show();
            }

            // Function to close other forms
            function closeOtherForms() {
                $('.auth-form').hide();
            }

            // Function to show the login form
            function openLoginForm() {
                showForm('#loginForm');
                closeOtherForms();
            }

            // Function to show the signup form
            function openSignupForm() {
                showForm('#signup-form');
                closeOtherForms();
            }

            // Function to show the forgot password form
            function openForgotPasswordForm() {
                showForm('#forgot-password-form');
                closeOtherForms();
            }

            // Your existing event listeners and functions
            // ...

            // Event listener for the signup link in the login form
            $('#login-link-signup').click(function () {
                openSignupForm();
            });

            $('#signup-link-login').click(function () {
                openLoginForm();
            });

            $('#login-link-forgot-password').click(function () {
                openForgotPasswordForm();
            });
        });

       // Function to fetch available packages based on selected destination and dates
        function fetchAvailablePackages() {
            const selectedDestination = document.getElementById('destinationSelect').value;
            const fromDate = document.getElementById('fromDateInput').value;
            const toDate = document.getElementById('toDateInput').value;

            fetch('/get_available_packages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    selected_destination: selectedDestination,
                    start_date: fromDate,
                    end_date: toDate
                })
            })
            .then(response => {
                console.log('Response Status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const packagesContainer = document.getElementById('packages_container');
                packagesContainer.innerHTML = ''; // Clear previous content
                if (data.success) {
                    data.packages.forEach(package => {
                        // Create elements to display package details and book now button
                        const packageDiv = document.createElement('div');
                        packageDiv.classList.add('package');
                        packageDiv.innerHTML = `
                            <h3>${package.hotel}</h3>
                            <p><strong>Place:</strong> ${package.place}</p>
                            <p><strong>Budget:</strong> ${package.budget}</p>
                            <p><strong>Guests:</strong> ${package.guest}</p>
                            <img src="${package.image_url}" alt="Package Image">
                            <button class="btn btn-primary book-now-btn" data-package-id="${package.id}">Book Now</button>
                        `;
                        packagesContainer.appendChild(packageDiv);
                    });

                    // Add event listener to book now buttons
                    document.addEventListener('DOMContentLoaded', function () {
                        const bookNowButtons = document.querySelectorAll('.book-now-btn');
                        bookNowButtons.forEach(button => {
                            button.addEventListener('click', function () {
                                const packageId = button.getAttribute('data-package-id');
                                // Redirect to the booking page with the selected package ID
                                window.location.href = '/booking_page?packageId=' + packageId;
                            });
                        });
                    });
                } else {
                    // Display message if no packages available
                    packagesContainer.innerHTML = '<p>No packages available for selected dates.</p>';
                }
            })
            .catch(error => {
                // Display error message in alert box
                alert('Error: ' + error.message);
                console.error('Error:', error);
            });
        }



        document.addEventListener('DOMContentLoaded', function () {
            // Fetch package details when the page loads
            fetchPackageDetails();
        });

        function fetchPackageDetails() {
            // Assuming you have a function to make an AJAX request to fetch package details
            // This function will depend on your backend implementation
            // Here's a basic example:
            fetch('/get_package_details')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        displayPackageDetails(data.packages);
                    } else {
                        console.error('Failed to fetch package details:', data.error);
                    }
                })
                .catch(error => console.error('Error fetching package details:', error));
        }

        function displayPackageDetails(packages) {
            const packageDetailsContainer = document.getElementById('packageDetails');
            packageDetailsContainer.innerHTML = ''; // Clear previous content

            packages.forEach(package => {
                const packageDiv = document.createElement('div');
                packageDiv.classList.add('package');
                packageDiv.innerHTML = `
                    <h2>${package.hotel}</h2>
                    <p><strong>Place:</strong> &#8377;${package.place}</p>
                    <p><strong>Budget:</strong> ${package.budget}</p>
                    <p><strong>Guests:</strong> ${package.guest}</p>
                    <img src="${package.image_url}" alt="Package Image">
                `;
                packageDetailsContainer.appendChild(packageDiv);
            });
        }




        $(document).ready(function() {
            // Function to fetch package details from the Flask backend
            function fetchPackageDetails() {
                $.ajax({
                    url: '/get_packages',
                    type: 'GET',
                    success: function(response) {
                        if (response.packages) {
                            // Iterate through each package and append its details to the HTML
                            response.packages.forEach(function(package) {
                                $('#packageList').append(
                                    `<div class="col-lg-4 col-md-6 mb-4">
                                        <div class="package-item bg-white mb-2">
                                            <img class="img-fluid" src="${package.image_url}" alt="">
                                            <div class="p-4">
                                                <div class="d-flex justify-content-between mb-3">
                                                    <small class="m-0"><i class="fa fa-map-marker-alt text-primary mr-2"></i>${package.location}</small>
                                                    <small class="m-0"><i class="fa fa-calendar-alt text-primary mr-2"></i>${package.days}</small>
                                                    <small class="m-0"><i class="fa fa-user text-primary mr-2"></i>${package.person} Person</small>
                                                </div>
                                                <a class="h5 text-decoration-none" href="">${package.name}</a>
                                                <div class="border-top mt-4 pt-4">
                                                    <div class="d-flex justify-content-between">
                                                        <h6 class="m-0"><i class="fa fa-star text-primary mr-2"></i>${package.ratings} <small>(250)</small></h6>
                                                        <h5 class="m-0">&#8377;${package.price}</h5>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>`
                                );
                            });
                            // Attach event listener to book now buttons
                            function bookPackage(packageId) {
                                // Display a message in an alert box when the button is clicked
                                alert('Book Now button clicked for package ID: ' + packageId);
                            }

                            // Attach event listener to book now buttons
                            $('.book-now-btn').on('click', function() {
                                const packageId = $(this).data('package-id');
                                console.log('Book Now clicked for package ID:', packageId);

                                // Call the bookPackage function to handle the booking process
                                bookPackage(packageId);
                            });
                                // Make an AJAX request to check if the user is logged in
                                $.ajax({
                                    url: '/check_login_status',
                                    type: 'GET',
                                    success: function(response) {
                                        if (response.logged_in) {
                                            // User is logged in, proceed with booking
                                            bookPackage(packageId);
                                        } else {
                                            openLoginForm();
                                        screenTop = 0;
                                        window.scrollTo({ top: screenTop, behavior: 'smooth' });
                                        }
                                    },
                                    error: function(xhr, status, error) {
                                        console.error('Error checking login status:', error);
                                        // Handle error appropriately
                                    }
                                });
                        } else {
                            console.error('Failed to fetch package details:', response.error);
                            // Handle error appropriately
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('Error fetching package details:', error);
                        // Handle error appropriately
                    }

                });
            }



function submitBooking(packageId, startDate, endDate) {
    // Check if user is logged in and retrieve user ID from session
    const userId = sessionStorage.getItem('user_id');
    if (!userId) {
        alert('Please log in to book the package.');
        return;
    }

    // Make AJAX request to submit the booking
    fetch('/submit_booking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            userId: sessionStorage.getItem('user_id'),
            packageId: sessionStorage.getItem('package_id'),
            startDate: startDate,
            endDate: endDate
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Booking successful');
            // Perform any additional actions after successful booking
        } else {
            if (data.error === 'Duplicate booking') {
                alert('Duplicate booking: You have already booked this package.');
            } else {
                alert('Booking failed: ' + data.error);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing the booking: ' + error); // Show error in an alert box
    });
}


            // Make an AJAX request to check if the user is logged in
            $.ajax({
                url: '/check_login_status',
                type: 'GET',
                success: function(response) {
                    if (response.logged_in) {
                        // User is logged in
                        // Proceed with fetching package details and attaching event listeners
                        fetchPackageDetails();
                    } else {
                        openLoginForm();
                                        screenTop = 0;
                                        window.scrollTo({ top: screenTop, behavior: 'smooth' });
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error checking login status:', error);
                    // Handle error appropriately
                }
            });
        });


        function fetchUserPayments() {
            $.ajax({
                url: '/get_user_payments',
                type: 'GET',
                success: function(response) {
                    if (response.success) {
                        renderUserPayments(response.payments);
                        // Close bookings section if it's open
                        $('#userBookingsContainer').hide();
                    } else {
                        alert('Failed to fetch payments: ' + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching payments:', error);
                }
            });
        }

        function fetchUserBookings() {
            // Make an AJAX request to fetch user bookings
            $.ajax({
                url: '/fetch_bookings',
                type: 'GET',
                success: function(response) {
                    if (response.success) {
                        renderUserBookings(response.bookings);
                        screendown = 1;
                        window.scrollTo({ down: screendown, behavior: 'smooth' });
                        // Close payments section if it's open
                        $('#paymentDetails').hide();
                    } else {
                        alert('Failed to fetch user bookings: ' + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching user bookings:', error);
                }
            });
        }


        function renderUserBookings(bookings) {
            // Clear previous bookings
            $('#userBookingsContainer').empty();

            // Create a container div for the bookings with fixed height and overflow
            var bookingsContainer = $('<div></div>').css({
                'max-height': '200px', // Adjust the max height as needed
                'overflow-y': 'auto'   // Enable vertical scrollbar if needed
            });

            // Iterate through bookings and render them in a list
            var bookingsList = $('<ul></ul>'); // Create a new unordered list
            bookings.forEach(function(booking) {
                // Create list item for each booking
                var listItem = $('<li></li>').html(
                    'Booking ID: ' + booking.id + '<br>' +
                    'Package ID: ' + booking.package_id + '<br>' +
                    'Start Date: ' + booking.start_date + '<br>' +
                    'End Date: ' + booking.end_date + '<br>' +
                    'Booking Date: ' + booking.booking_date + '<br>' +
                    'booking_status :' + booking.booking_status + '<br>' +

                    '<button class="cancelBtn" data-booking-id="' + booking.id + '">Cancel</button>'
                );

                // Append list item to the bookings list
                bookingsList.append(listItem);
            });

            // Append the bookings list to the container
            bookingsContainer.append(bookingsList);

            // Append the container to the user bookings container
            $('#userBookingsContainer').append(bookingsContainer);

            // Attach event handler for cancel buttons
            $('.cancelBtn').click(function() {
                var bookingId = $(this).data('booking-id');
                cancelBooking(bookingId);
            });
            $('#userBookingsContainer').show(); // Show bookings section
            $('#paymentDetails').hide(); // Hide payments section
        }

        function cancelBooking(bookingId) {
            // Make an AJAX request to cancel the booking
            $.ajax({
                url: '/cancel_booking',
                type: 'POST',
                data: { booking_id: bookingId },
                success: function(response) {
                    if (response.success) {
                        alert(response.message);
                        fetchUserBookings(); // Refresh the list of bookings
                    } else {
                        alert('Failed to cancel booking: ' + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error cancelling booking:', error);
                }
            });
        }

        $(document).ready(function() {
            fetchUserBookings(); // Fetch user bookings when the page loads
        });



        function renderUserPayments(payments) {
            $('#paymentDetails').empty(); // Clear previous payment details
            $('#paymentDetails').show(); // Show payments section
            $('#userBookingsContainer').hide(); // Hide bookings section

    payments.forEach(function(payment) {
        var paymentItem = $('<div></div>').addClass('payment-item').html(
            '<p>Transaction ID: ' + payment.transaction_id + '</p>' +
            '<p>Payment Status: ' + payment.payment_status + '</p>'
        );

        if (payment.payment_status === 'success') {
            var refundBtn = $('<button></button>').addClass('action-button').text('Refund').click(function() {
                showRefundForm(payment.transaction_id);
            });
            paymentItem.append(refundBtn);
        } else if (payment.payment_status === 'pending') {
            var retryBtn = $('<button></button>').addClass('action-button').text('Retry').click(function() {
                retryPayment(payment.transaction_id);
            });
            paymentItem.append(retryBtn);
        }

        $('#paymentDetails').append(paymentItem);
    });
}


function showRefundForm(transactionId) {
    $('#refundFormContainer').empty(); // Clear previous form (if any)
    var refundForm = $('<form></form>').attr('id', 'refundForm');
    refundForm.append(
        $('<label></label>').attr('for', 'bankAccount').text('Bank Account:'),
        $('<input>').attr({ type: 'text', id: 'bankAccount', name: 'bankAccount', required: true }),
        $('<button></button>').attr({ type: 'submit', id: 'refundSubmit' }).text('Submit Refund')
    );

    // Handle form submission
    refundForm.on('submit', function(e) {
        e.preventDefault(); // Prevent default form submission
        submitRefundForm(transactionId); // Call the function to submit refund via AJAX
    });

    $('#refundFormContainer').append(refundForm);

    // Show the refund modal
    $('#refundModal').show();

    // Close modal when the close button is clicked
    $('.close').on('click', function() {
        $('#refundModal').hide();
    });
}

// Ensure the document is ready before executing this script
$(document).ready(function() {
    // Other functions and AJAX requests are here...
    $(document).ready(function() {
        $('#ifscCode').on('change', function() {
            var ifscCode = $(this).val();
            // Make AJAX request to fetch bank name based on IFSC code
            $.ajax({
                url: '/get_bank_name',
                type: 'POST',
                data: { ifscCode: ifscCode },
                success: function(response) {
                    $('#bankName').text('Bank Name: ' + response.bank_name);
                },
                error: function(xhr, status, error) {
                    console.error('Error fetching bank name:', error);
                }
            });
        });
    });

    // Check if the form submission event is triggered
    $('#refundSubmit').on('click', function(e) {
        e.preventDefault(); // Prevent default button behavior
        console.log('Submit button clicked'); // Check in the console if this message appears
    });
});


function submitRefundForm(transactionId) {
    var bankAccount = $('#bankAccount').val();
    $.ajax({
        url: '/process_refund',
        type: 'POST',
        data: JSON.stringify({ transaction_id: transactionId, bank_account: bankAccount }),
        contentType: 'application/json',
        success: function(response) {
            $('#refundMessage').text(response.message);
        },
        error: function(xhr, status, error) {
            console.error('Error processing refund:', error);
        }
    });
}

function retryPayment(transactionId) {
    $.ajax({
        url: '/retry_payment',
        type: 'POST',
        data: JSON.stringify({ transaction_id: transactionId }),
        contentType: 'application/json',
        success: function(response) {
            alert(response.message);
            fetchUserPayments(); // Refresh payment details
        },
        error: function(xhr, status, error) {
            console.error('Error retrying payment:', error);
        }
    });
}

$(document).ready(function() {
    fetchUserPayments(); 
    // Event listener for refund button click
    $(document).on('click', '.refund-button', function() {
        var transactionId = $(this).data('transaction-id');
        showRefundForm(transactionId);
    });

    // Event listener for retry button click
    $(document).on('click', '.retry-button', function() {
        var transactionId = $(this).data('transaction-id');
        retryPayment(transactionId);
    });// Fetch user payments on page load
});



