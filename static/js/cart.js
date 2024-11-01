
$(document).ready(function() {
    $('.quantity').on('input', function() {
        var itemId = $(this).data('item-id'); // Get CartItem ID
        var newQuantity = $(this).val();

        $.ajax({
            url: '/cart/update_cart/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'item_id': itemId,
                'new_quantity': newQuantity
            },
            success: function(response) {
                console.log(response);
                if (response.success) {
                    
                    console.log('Quantity updated successfully.');
                    $('.cart-total').text(`$${response.cart_total.toFixed(2)}`);
                    $(`#product-total-${itemId}`).text(`$${response.item_total.toFixed(2)}`);
                    console.log("Updating product total:", `#product-total-${itemId}`, `$${response.item_total.toFixed(2)}`);

                    // You may also update the total price dynamically here if needed
                } else {
                    alert(response.message);
                }
            },
            error: function() {
                alert('An error occurred. Please try again.');
            }
        });
    });
});


    // document.addEventListener("DOMContentLoaded", function () {
    //     // Function to update cart item quantity
    // Function to remove cart item
    document.querySelectorAll(".product-remove a").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            const variantId = this.href.split("/").pop();

            $.ajax({
                url: `/remove_from_cart/${variantId}/`, // Adjust based on your remove URL structure
                type: "POST",
                data: {
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (response) {
                    $(`#cart-item-${variantId}`).remove(); // Remove item from DOM
                    $("#cart-total").text(`$${response.total_price.toFixed(2)}`);
                },
                error: function () {
                    alert("Failed to remove cart item.");
                }
            });
        });
    });
// });
