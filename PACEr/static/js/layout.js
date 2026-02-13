// Nav toggle with smooth animation
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('nav-toggle');
    const content = document.getElementById('nav-content');

    if (toggle && content) {
        toggle.addEventListener('click', function() {
            content.classList.toggle('hidden');
        });
    }

    // Viewport height for mobile
    const setVh = () => {
        document.documentElement.style.setProperty('--vh', `${window.innerHeight * 0.01}px`);
    };
    setVh();
    window.addEventListener('resize', setVh);
});
