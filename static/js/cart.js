
$(document).ready(function() {
    $('.quantity').on('input', function() {
        var itemId = $(this).data('item-id'); 
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
                if (response.success) {
                    $('.cart-total').text(`$${response.cart_total.toFixed(2)}`);
                    $(`#product-total-${itemId}`).text(`$${response.item_total.toFixed(2)}`);
   
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



$(document).ready(function() {
    $('.remove-from-cart').on('click', function() {
        var itemId = $(this).data('item-id');

        $.ajax({
            url: '/cart/remove_from_cart/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'item_id': itemId
            },
            success: function(response) {
                if (response.success) {
                    // Remove the item row from the cart
                    $('#cart-item-' + itemId).remove();

                    // Update the cart total
                    $('.cart-total').text(`$${response.cart_total.toFixed(2)}`);
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
