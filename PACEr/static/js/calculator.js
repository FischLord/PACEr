// Unified calculator validation
var MAX_LENGTH = 100000;

var kmhRanges = {
    'hindernisstrecke': { min: 8, max: 14 },
    'wegstrecke': { min: 8, max: 15 },
    'schrittstrecke': { min: 3, max: 7 }
};

function updateKmhTicks(min, max) {
    var container = document.getElementById('kmh-ticks');
    if (!container) return;
    container.innerHTML = '';
    for (var i = min; i <= max; i++) {
        var tick = document.createElement('div');
        tick.className = 'slider-tick';
        container.appendChild(tick);
    }
}

function updateKmhOptions(art) {
    var kmhSlider = document.getElementById('kmh');
    var kmhValue = document.getElementById('kmh-value');
    var kmhMinLabel = document.getElementById('kmh-min-label');
    var kmhMaxLabel = document.getElementById('kmh-max-label');
    var tempoField = document.getElementById('tempoInputField');
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
        updateKmhTicks(range.min, range.max);
        tempoField.style.display = '';
    } else {
        tempoField.style.display = 'none';
    }
}

// Radio button change handler for art chips
document.addEventListener('change', function(e) {
    if (e.target.name === 'art' && e.target.type === 'radio') {
        updateKmhOptions(e.target.value);
    }
});

// Slider live value display
document.addEventListener('input', function(e) {
    if (e.target.id === 'kmh' && e.target.type === 'range') {
        var kmhValue = document.getElementById('kmh-value');
        if (kmhValue) kmhValue.textContent = e.target.value;
    }
});

// Validate length input
document.addEventListener('input', function(e) {
    if (e.target.id !== 'laenge') return;
    var val = parseInt(e.target.value);
    var errEl = document.getElementById('laenge-error');
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

// Mode toggle — segmented control with sliding indicator
document.addEventListener('htmx:afterSwap', function(e) {
    if (e.detail.target.id === 'form-area') {
        var trigger = e.detail.requestConfig.elt;
        var btnAuto = document.getElementById('btn-auto');
        var btnManuell = document.getElementById('btn-manuell');
        var indicator = document.getElementById('toggle-indicator');

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

        // Slide the indicator
        if (indicator) {
            if (trigger.id === 'btn-auto') {
                indicator.style.left = '4px';
                indicator.style.width = 'calc(50% - 4px)';
            } else {
                indicator.style.left = 'calc(50%)';
                indicator.style.width = 'calc(50% - 4px)';
            }
        }
    }
});
