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

