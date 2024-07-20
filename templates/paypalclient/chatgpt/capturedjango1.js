
    paypal.Buttons({
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: '10.00' // Replace with actual amount
                    }
                }]
            });
        },
        onApprove: function(data, actions) {
            // Capture the payment on client side
            return actions.order.capture().then(function(details) {
                // Log the details to console
                console.log(details);

                // Send a fetch API request to Django backend
                fetch('/your_django_endpoint/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        orderID: data.orderID,
                        payerID: details.payer.payer_id,
                        paymentID: details.purchase_units[0].payments.captures[0].id,
                        amount: details.purchase_units[0].amount.value,
                        // Include any other relevant details
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    // Handle success response from Django (e.g., redirect, show confirmation)
                    alert('Transaction completed by ' + details.payer.name.given_name);
                    // Example: window.location.href = '/thank-you/';
                })
                .catch((error) => {
                    console.error('Error:', error);
                    // Handle error response from Django (e.g., show error message)
                    alert('Transaction failed. Please try again.');
                });
            });
        }
    }).render('#paypal-button-container');

