// File: refreshOnBack.js
document.addEventListener("DOMContentLoaded", function() {
    window.addEventListener("pageshow", function(event) {
        if (event.persisted) {  // Check if the page was loaded from cache
            window.location.reload();  // Reload the page from the server
        }
    });
});
