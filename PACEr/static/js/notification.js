// Toast notification system
window.showToast = function(title, message, duration) {
    duration = duration || 5000;
    var container = document.getElementById('toast-container');
    if (!container) return;

    var toast = document.createElement('div');
    toast.className = 'bg-surface-raised border border-surface-border rounded-xl shadow-xl p-4 min-w-[280px] max-w-sm animate-toast-in';
    toast.innerHTML =
        '<div class="flex items-start gap-3">' +
            '<div class="flex-1">' +
                '<p class="font-semibold text-accent text-sm">' + title + '</p>' +
                '<p class="text-text-secondary text-sm mt-1">' + message + '</p>' +
            '</div>' +
            '<button class="text-text-muted hover:text-text-primary transition-colors flex-shrink-0" onclick="this.closest(\'.animate-toast-in, [class*=toast]\').remove()">' +
                '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>' +
            '</button>' +
        '</div>';

    container.appendChild(toast);

    // Auto-dismiss
    setTimeout(function() {
        toast.classList.remove('animate-toast-in');
        toast.classList.add('animate-toast-out');
        setTimeout(function() { toast.remove(); }, 300);
    }, duration);
};
