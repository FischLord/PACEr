// Unified calculator validation
var MAX_LENGTH = 100000;

var kmhRanges = {
    'hindernisstrecke': { min: 8, max: 14 },
    'wegstrecke': { min: 8, max: 15 },
    'schrittstrecke': { min: 3, max: 7 }
};

function updateKmhTicks(min, max, form) {
    var container = form.querySelector('[data-kmh-ticks]');
    if (!container) return;
    container.innerHTML = '';
    for (var i = min; i <= max; i++) {
        var tick = document.createElement('div');
        tick.className = 'slider-tick';
        container.appendChild(tick);
    }
}

function updateKmhOptions(art, form) {
    if (!form) return;
    var kmhSlider = form.querySelector('[data-kmh-slider]');
    var kmhValue = form.querySelector('[data-kmh-value]');
    var kmhMinLabel = form.querySelector('[data-kmh-min-label]');
    var kmhMaxLabel = form.querySelector('[data-kmh-max-label]');
    var tempoField = form.querySelector('[data-tempo-field]');
    if (!kmhSlider || !tempoField) return;

    var range = kmhRanges[art];
    if (range) {
        kmhSlider.min = range.min;
        kmhSlider.max = range.max;
        kmhSlider.step = 1;
        // Set default to middle of range
        var mid = Math.round((range.min + range.max) / 2);
        kmhSlider.value = mid;
        if (kmhValue) kmhValue.textContent = mid;
        if (kmhMinLabel) kmhMinLabel.textContent = range.min + ' km/h';
        if (kmhMaxLabel) kmhMaxLabel.textContent = range.max + ' km/h';
        updateKmhTicks(range.min, range.max, form);
        tempoField.style.display = '';
    } else {
        tempoField.style.display = 'none';
    }
}

function initializeSelectedArt(root) {
    var scope = root || document;
    var forms = scope.matches && scope.matches('.form-calculator')
        ? [scope]
        : scope.querySelectorAll('.form-calculator');

    for (var i = 0; i < forms.length; i++) {
        var selectedArt = forms[i].querySelector('input[name="art"]:checked');
        if (selectedArt) {
            updateKmhOptions(selectedArt.value, forms[i]);
        }
    }
}

document.addEventListener('DOMContentLoaded', initializeSelectedArt);

function moveToggleIndicator(activeButton) {
    var indicator = document.getElementById('toggle-indicator');
    var toggle = indicator ? indicator.parentElement : null;
    if (!indicator || !toggle || !activeButton) return;

    var toggleRect = toggle.getBoundingClientRect();
    var buttonRect = activeButton.getBoundingClientRect();
    indicator.style.left = (buttonRect.left - toggleRect.left) + 'px';
    indicator.style.width = buttonRect.width + 'px';
}

document.addEventListener('DOMContentLoaded', function() {
    var activeButton = document.querySelector('#btn-auto.text-white, #btn-manuell.text-white');
    moveToggleIndicator(activeButton);
});

window.addEventListener('resize', function() {
    var activeButton = document.querySelector('#btn-auto.text-white, #btn-manuell.text-white');
    moveToggleIndicator(activeButton);
});

// Radio button change handler for art chips
document.addEventListener('change', function(e) {
    if (e.target.name === 'art' && e.target.type === 'radio') {
        updateKmhOptions(e.target.value, e.target.closest('.form-calculator'));
    }
});

// Slider live value display
document.addEventListener('input', function(e) {
    if (e.target.name === 'kmh' && e.target.type === 'range') {
        var form = e.target.closest('.form-calculator');
        var kmhValue = form ? form.querySelector('[data-kmh-value]') : null;
        if (kmhValue) kmhValue.textContent = e.target.value;
    }
});

// Validate length input
document.addEventListener('input', function(e) {
    if (e.target.name !== 'laenge') return;
    var val = parseInt(e.target.value);
    var form = e.target.closest('.form-calculator');
    var errEl = form ? form.querySelector('[data-laenge-error]') : null;
    if (!errEl) return;

    if (val <= 0 || val > MAX_LENGTH || isNaN(val)) {
        errEl.classList.remove('hidden');
    } else {
        errEl.classList.add('hidden');
    }
});

// Validate seconds fields (manual mode)
document.addEventListener('input', function(e) {
    if (e.target.type !== 'number' || !e.target.name || !e.target.name.endsWith('_sec')) return;
    var val = parseInt(e.target.value);
    var container = e.target.closest('.mb-5, .mb-6');
    if (!container) return;
    var errEl = container.querySelector('[id$="-error"]');
    if (!errEl) return;

    if (val < 0 || val > 59) {
        errEl.classList.remove('hidden');
    } else {
        errEl.classList.add('hidden');
    }
});

// Initialize dependent tempo controls after HTMX replaces the form.
document.addEventListener('htmx:afterSwap', function(e) {
    initializeSelectedArt(e.detail.target);
});

// Mode toggle — segmented control with sliding indicator
document.addEventListener('htmx:afterSwap', function(e) {
    if (e.detail.target.id === 'form-area') {
        var trigger = e.detail.requestConfig.elt;
        if (!trigger || (trigger.id !== 'btn-auto' && trigger.id !== 'btn-manuell')) return;

        var btnAuto = document.getElementById('btn-auto');
        var btnManuell = document.getElementById('btn-manuell');
        if (btnAuto && btnManuell) {
            // Reset both buttons
            btnAuto.classList.remove('text-white');
            btnAuto.classList.add('text-text-secondary');
            btnManuell.classList.remove('text-white');
            btnManuell.classList.add('text-text-secondary');

            // Activate triggered button
            trigger.classList.add('text-white');
            trigger.classList.remove('text-text-secondary');
        }

        moveToggleIndicator(trigger);
    }
});

// Prevent accidental duplicate calculations while a mobile request is still pending.
document.addEventListener('htmx:beforeRequest', function(e) {
    if (!e.detail.elt || !e.detail.elt.classList.contains('form-calculator')) return;
    var submitButton = e.detail.elt.querySelector('.submit-button');
    if (!submitButton) return;
    submitButton.disabled = true;
    submitButton.classList.add('opacity-70', 'cursor-wait');
});

document.addEventListener('htmx:afterRequest', function(e) {
    if (!e.detail.elt || !e.detail.elt.classList.contains('form-calculator')) return;
    var submitButton = e.detail.elt.querySelector('.submit-button');
    if (!submitButton) return;
    submitButton.disabled = false;
    submitButton.classList.remove('opacity-70', 'cursor-wait');
});
