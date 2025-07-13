$(document).ready(function() {
    // Function to fetch package details and display them
    function fetchPackageDetails() {
        $.ajax({
            url: '/fetch_package_details',  // Route to fetch package details
            type: 'GET',
            data: { packageId: 'your_package_id' },  // Replace 'your_package_id' with actual package ID
            success: function(response) {
                if (response.success) {
                    // Display package details in the HTML
                    const packageDetails = response.packageDetails;
                    $('#packageDetails').append(`
                        <p>Package ID: ${packageDetails.id}</p>
                        <p>Destination: ${packageDetails.destination}</p>
                        <p>Start Date: ${packageDetails.startDate}</p>
                        <p>End Date: ${packageDetails.endDate}</p>
                        <p>Price: ${packageDetails.price}</p>
                    `);
                } else {
                    console.error('Error fetching package details:', response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('Error fetching package details:', error);
            }
        });
    }

    // Call fetchPackageDetails function when the page loads
    fetchPackageDetails();

    // Function to handle payment process when Pay Now button is clicked
    $('#payNowBtn').click(function() {
        // Perform payment process (You can add your payment gateway integration logic here)
        $.ajax({
            url: '/process_payment',  // Route to process payment (implement this route in your Flask app)
            type: 'POST',
            data: { packageId: 'your_package_id' },  // Replace 'your_package_id' with actual package ID
            success: function(response) {
                if (response.success) {
                    // Payment successful, proceed with booking
                    alert('Payment successful! Booking will be completed.');
                    window.location.href = '/submit_booking';  // Redirect to submit booking route
                } else {
                    // Payment failed, show error message
                    alert('Payment failed. Please try again or contact support.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error processing payment:', error);
                alert('Error processing payment. Please try again or contact support.');
            }
        });
    });
});
