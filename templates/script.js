// Existing JavaScript code
// ...

// Handle Menu Item Clicks
document.querySelectorAll('.menu ul li a').forEach(function(element) {
    element.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default link behavior
        const popup = document.getElementById('popup');
        const popupText = document.getElementById('popup-text');
        const linkText = this.textContent.trim();

        // Set the content based on which link was clicked
        if (linkText === 'Help') {
            popupText.innerHTML = '<h2>Help</h2><p>This is the help section.</p>';
        } else if (linkText === 'Setting') {
            popupText.innerHTML = '<h2>Setting</h2><p>This is the settings section.</p>';
        } else if (linkText === 'About Us') {
            popupText.innerHTML = '<h2>About Us</h2><p>This is the about us section.</p>';
        } else {
            popupText.innerHTML = '<h2>Info</h2><p>Additional information.</p>';
        }

        // Display the pop-up
        popup.style.display = 'block';
    });
});

// Close Pop-up When Clicking on Close Button
document.querySelector('.close').addEventListener('click', function() {
    document.getElementById('popup').style.display = 'none';
});

// Close Pop-up When Clicking Outside the Pop-up Content
window.addEventListener('click', function(event) {
    const popup = document.getElementById('popup');
    if (event.target === popup) {
        popup.style.display = 'none';
    }
});
