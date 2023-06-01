//? Javascript to toggle the Burger menu
document.getElementById("nav-toggle").onclick = function () {
    document.getElementById("nav-content").classList.toggle("hidden");
};

// Get viewport height
let vh = window.innerHeight * 0.01;
// Set document variable
document.documentElement.style.setProperty("--vh", `${vh}px`);
// On window resize, recalculate viewport height
window.addEventListener("resize", () => {
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty("--vh", `${vh}px`);
});

// Get references to the popup and close button
const popup = document.getElementById('popup');
const closeBtn = document.getElementById('closeBtn');

// Function to close the popup
function closePopup() {
  popup.style.display = 'none';
}

// Add event listener to the close button
closeBtn.addEventListener('click', closePopup);