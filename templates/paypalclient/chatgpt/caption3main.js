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
            // Send a fetch API request to Django backend to process payment capture
            return fetch('/capture_payment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    orderID: data.orderID
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Transaction completed by ' + data.payerName);
                    // Example: redirect to a thank-you page
                    // window.location.href = '/thank-you/';
                } else {
                    alert('Transaction failed. Please try again.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Transaction failed. Please try again.');
            });
        }
    }).render('#paypal-button-container');
