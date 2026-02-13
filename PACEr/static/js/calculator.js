// Unified calculator validation
var MAX_LENGTH = 100000;

function updateKmhOptions(art) {
    var kmhSelect = document.getElementById('kmh');
    var tempoField = document.getElementById('tempoInputField');
    if (!kmhSelect || !tempoField) return;

    // Clear existing options
    kmhSelect.innerHTML = '<option value="" disabled selected>Bitte wählen</option>';

    var ranges = {
        'hindernisstrecke': { min: 8, max: 14 },
        'wegstrecke': { min: 8, max: 15 },
        'schrittstrecke': { min: 3, max: 7 }
    };

    var range = ranges[art];
    if (range) {
        for (var i = range.min; i <= range.max; i++) {
            var opt = document.createElement('option');
            opt.value = i;
            opt.textContent = i + ' km/h';
            kmhSelect.appendChild(opt);
        }
        tempoField.style.display = '';
    } else {
        tempoField.style.display = 'none';
    }
}

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

// Mode toggle button styling
document.addEventListener('htmx:afterSwap', function(e) {
    if (e.detail.target.id === 'form-area') {
        // Update button styles
        var trigger = e.detail.requestConfig.elt;
        var btns = document.querySelectorAll('#btn-auto, #btn-manuell');
        btns.forEach(function(btn) {
            btn.classList.remove('bg-orange-600', 'text-white');
            btn.classList.add('text-gray-400', 'hover:text-gray-300');
        });
        trigger.classList.add('bg-orange-600', 'text-white');
        trigger.classList.remove('text-gray-400', 'hover:text-gray-300');
    }
});
