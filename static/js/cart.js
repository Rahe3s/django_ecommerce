
function updateCart(variantUid) {
    const quantityElement = document.getElementById('quantity');
    const resultElement = document.getElementById('result');
    
    // Ensure necessary elements are present
    if (!quantityElement || !resultElement) return;

    const quantity = quantityElement.value;
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    
    // Abort if CSRF token is missing
    if (!csrfTokenElement) return;

    const csrfToken = csrfTokenElement.value;

    fetch(`/cart/update_cart/${variantUid}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.ok ? response.json() : Promise.reject())
    .then(data => {
        // Update result if successful, or show an error message
        resultElement.innerHTML = data.success
            ? `<p>${data.message}</p><p>New Quantity: ${data.new_quantity}</p><p>Total Price: $${data.total_price}</p>`
            : `<p>${data.message}</p>`;
    })
    .catch(() => {
        // Display a generic error message
        resultElement.innerHTML = `<p>There was an error processing your request. Please try again later.</p>`;
    });
}

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
