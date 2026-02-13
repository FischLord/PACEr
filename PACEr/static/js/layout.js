// Mobile menu with slide-in overlay
document.addEventListener('DOMContentLoaded', function() {
    var toggle = document.getElementById('nav-toggle');
    var close = document.getElementById('nav-close');
    var overlay = document.getElementById('nav-overlay');
    var backdrop = document.getElementById('nav-backdrop');
    var panel = document.getElementById('nav-panel');

    function openMenu() {
        if (!overlay || !backdrop || !panel) return;
        overlay.classList.remove('pointer-events-none');
        overlay.setAttribute('aria-hidden', 'false');
        backdrop.classList.remove('opacity-0');
        backdrop.classList.add('opacity-100');
        panel.classList.remove('translate-x-full');
        panel.classList.add('translate-x-0');
        if (toggle) toggle.setAttribute('aria-expanded', 'true');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        if (!overlay || !backdrop || !panel) return;
        backdrop.classList.remove('opacity-100');
        backdrop.classList.add('opacity-0');
        panel.classList.remove('translate-x-0');
        panel.classList.add('translate-x-full');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
        setTimeout(function() {
            overlay.classList.add('pointer-events-none');
            overlay.setAttribute('aria-hidden', 'true');
        }, 300);
    }

    if (toggle) toggle.addEventListener('click', openMenu);
    if (close) close.addEventListener('click', closeMenu);
    if (backdrop) backdrop.addEventListener('click', closeMenu);

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeMenu();
    });

    // Close on link click inside panel
    if (panel) {
        panel.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') closeMenu();
        });
    }

    // Viewport height for mobile
    var setVh = function() {
        document.documentElement.style.setProperty('--vh', window.innerHeight * 0.01 + 'px');
    };
    setVh();
    window.addEventListener('resize', setVh);

    // IntersectionObserver for stagger animations
    var staggerItems = document.querySelectorAll('.stagger-item');
    if (staggerItems.length > 0 && 'IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        staggerItems.forEach(function(item) { observer.observe(item); });
    }
});
