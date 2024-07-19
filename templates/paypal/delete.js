// Function to initialize PayPal Hosted Fields
function initializeHostedFields(clientToken) {
    paypal.HostedFields.render({
        createOrder: function () {
            return fetch('{% url "paypal:create_order" %}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    payment_method: 'credit_card',
                    item_name: '',
                    item_sku: '',
                    item_price: '',
                    item_currency: '',
                    item_quantity: ''
                })
            }).then(response => response.json())
                .then(orderData => orderData.id)
                .catch(error => {
                    console.error('Failed to create order:', error);
                });
        },
        styles: {
            'input': {
                'font-size': '16px',
                'color': '#3A3A3A'
            },
            ':focus': {
                'color': '#333333'
            }
        },
        fields: {
            number: {
                selector: '#card-number',
                placeholder: 'Card Number'
            },
            cvv: {
                selector: '#cvv',
                placeholder: 'CVV'
            },
            expirationDate: {
                selector: '#expiration-date',
                placeholder: 'MM/YY'
            }
        },
        authorization: clientToken
    }).then(function (hostedFieldsInstance) {
        document.querySelector('#payment__btn').addEventListener('click', function (event) {
            event.preventDefault();
            hostedFieldsInstance.submit().then(function (payload) {
                console.log('Payment successful:', payload);
                // Submit payload to your server to complete the payment
                return fetch('{% url "paypal:execute_payment" %}', {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    body: JSON.stringify(payload)
                }).then(function(res) {
                    return res.json();
                }).then(function(data) {
                    if (data.status === 'success') {
                        alert('Payment completed successfully!');
                    } else {
                        alert('Payment failed: ' + data.message);
                    }
                });
            }).catch(function (error) {
                console.error('Payment submission error:', error);
                // Handle error as needed
            });
        });
    }).catch(function (error) {
        console.error('Failed to initialize PayPal Hosted Fields:', error);
    });
}



<!-- <div id="credit-card-fields" style="display: none;">
                            <p class="text-white">Toggled On</p>
                            <div id="card-number" class="hosted-field"></div>
                            <div id="cvv" class="hosted-field"></div>
                            <div id="expiration-date" class="hosted-field"></div>
                        </div> -->