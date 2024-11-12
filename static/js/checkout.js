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
    $("#toggle-address-form").on("click", function () {
        addressForm.toggle(); // Show/hide the address form
        addressList.hide(); // Hide the list if it's open
    });

      
   
});

$(document).ready(function () {
    const addressForm = $("#address");
    const addressListContainer = $("#address-list ul");  // The container to hold the list of addresses

    // Handle Address Form Submission via AJAX
    addressForm.on("submit", function (event) {
        event.preventDefault();  // Prevent the form's default submission

        const formData = addressForm.serialize();  // Serialize form data
        console.log("Serialized Form Data:", formData);  // Debugging

        $.ajax({
            url: '/checkout/add_address/',  // Adjust URL as per your Django URL configuration
            type: 'POST',
            data: formData,  // Send serialized form data
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                if (data.success) {
                    // Clear the current address list
                    addressListContainer.empty();

                    // Iterate through the returned addresses and create radio buttons for each address
                    $.each(data.addresses.slice(0,3), function (index, address) {
                        const radioButton = `
                            <li class="mb-2">
                        <div class="p-2 border rounded bg-white">
                            <label class="d-flex align-items-center">
                                <input type="radio" name="selected_address" value="{{ address.uid }}" required class="me-2">
                                <span>
                                    {{ address.name }} - {{ address.address }}, {{ address.place }}, {{ address.state }}, {{ address.PIN }}
                                </span>
                            </label>
                        </div>
                    </li>
                        `;
                        addressListContainer.append(radioButton);
                    });

                    // Reset form and toggle visibility
                    addressForm[0].reset();
                    addressForm.hide();
                    $("#address-list").show();  // Show the updated address list
                } else {
                    alert("Failed to add address. Please check the form.");
                    console.error("Errors:", data.errors);
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX error:", status, error);
                alert("An error occurred. Please try again.");
            }
        });
    });
});
