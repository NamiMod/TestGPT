// On page load, animate the card into view
window.onload = function() {
    const card = document.querySelector('.card');
    setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
    }, 100);
};

// Show results when typing in the input field
const searchInput = document.getElementById('search-input');
const resultsArea = document.getElementById('results-area');
