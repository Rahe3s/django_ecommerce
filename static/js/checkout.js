$(document).ready(function() {
    $('#apply_coupon').on('click', function(event) {
        event.preventDefault(); // Prevents form submission

        var couponUid = $('#coupon').val();
        var cart_total = parseFloat($('#cart-total').data('cart-total'));
        console.log("Selected cart-total:", cart_total);
         // Get selected coupon UID
        console.log("Selected Coupon UID:", couponUid); // Log the UID for debugging

        // Check if a coupon is selected
        if (!couponUid) {
            alert("Please select a coupon.");
            return;
        }

        $.ajax({
            url: '/checkout/apply_coupon/',  // Ensure this URL matches your Django URL configuration
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'coupon_uid': couponUid ,
                'cart_total': cart_total // Pass the coupon UID here
            },
            success: function(response) {
                console.log("Server response:", response); // Log the response for debugging

                if (response.success) {
                    // Update discount and total fields based on response
                    $('#discount').text(`${response.discount.toFixed(2)}`);
                    $('#order_total').text(`${response.order_total.toFixed(2)}`);
                } else {
                    alert(response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error("AJAX error:", status, error); // Log any AJAX errors
                alert('An error occurred. Please try again.');
            }
        });
    });
});
