   // Sidebar Toggler
   $('.sidebar-toggler').click(function () {
    $('.sidebar, .content').toggleClass("open");
    return false;
});

$(document).ready(function() {
    // Handle click events for dynamic links
    $('.nav-item a').click(function(event) {
        event.preventDefault(); // Prevent the default action
        var url = $(this).attr('href'); // Get the URL from the link

        // Load the content dynamically via AJAX
        $.ajax({
            url: url,
            success: function(data) {
                // Replace the dynamic content block with the new content
                $('#dynamic-content').html(data);
            },
            error: function(xhr) {
                console.log("Error loading content: " + xhr.status + " " + xhr.statusText);
            }
        });
    });
});
    