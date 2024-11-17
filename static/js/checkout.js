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
    const addressList = $("#address-list");
    const addressForm = $("#address-form");


    // Toggle Address List
   

    // Toggle Address Form
    // $("#toggle-address-form").on("click", function () {
    //     addressForm.toggle(); // Show/hide the address form
    //     addressList.hide(); // Hide the list if it's open
    // });

      
   
});

$(document).ready(function () {
    // Toggle the address form display
    $("#toggle-address-form").click(function () {
        $("#address-form").toggle();
    });

    // AJAX submission for adding a new address
    $("#address").on("submit", function (e) {
        e.preventDefault(); // Prevent the form from submitting normally

        $.ajax({
            type: "POST",
            url: "/checkout/add_address/", // URL for the AJAX request
            data: $(this).serialize(), // Send form data with CSRF token
            success: function (response) {
                if (response.success) {
                    // Reload the address list by updating the inner HTML
                    $("#address-list").html(response.address_list_html);
                    $("#address-form").hide(); // Hide the form after successful submission
                    $("#address")[0].reset(); // Clear the form
                } else {
                    // Display error messages if there are validation errors
                    alert("Error: " + JSON.stringify(response.errors));
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX Error:", error);
                alert("An error occurred. Please try again.");
            },
        });
        
    });
    $('.btn-primary.btn-lg.btn-block').click(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/order/place_order/',
            data: {
                'selected_address': $('input[name="selected_address"]:checked').val(),
                'coupon': $('#coupon').val(),
                'payment_method': $('input[name="payment_method"]:checked').val(),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            },
            success: function(response) {
                if (response.status === 'success') {
                    
                    window.location.href = '/order/success/'+response.order_id; ;  // Redirect to success page
                } else if (response.status === 'redirect') {
                    window.location.href = response.url;  // Redirect to payment page
                } else {
                    alert(response.message);  // Show error message
                }
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);  // Debugging errors
                alert('An error occurred. Please try again.');
            }
        });
    });
});




