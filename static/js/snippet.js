    window.onload = function() {
        var inputs = document.querySelectorAll('input[type="text"], input[type="password"], textarea');
        inputs.forEach(function(input) {
            input.value = ''; // Clear the value of each input field
        });
    };

