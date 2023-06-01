// Get references to the popup and close button
const popup = document.getElementById('popup');
const closeBtn = document.getElementById('closeBtn');

// Function to close the popup
function closePopup() {
  popup.style.display = 'none';
}

// Add event listener to the close button
closeBtn.addEventListener('click', closePopup);