// static/js/shop.js

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const categoryFilter = document.getElementById("categoryFilter");
    const productContainer = document.getElementById("productContainer");
  
    function fetchFilteredProducts() {
      const searchQuery = searchInput.value;
      const categoryId = categoryFilter.value;
  
      fetch(`/shop/filter/?search=${searchQuery}&category=${categoryId}`)
        .then((response) => response.json())
        .then((data) => {
          productContainer.innerHTML = data.html;
        })
        .catch((error) => console.error("Error fetching products:", error));
    }
  
    searchInput.addEventListener("input", fetchFilteredProducts);
    categoryFilter.addEventListener("change", fetchFilteredProducts);
    console.log("Selected category UID:", categoryFilter.value);
  });
  