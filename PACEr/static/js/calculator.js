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

// Client-first calculation flow.
// The browser renders immediately. When online, the server recalculates and
// persists in the background, then returns the authoritative PDF URL.
(function() {
    function isClientCalculationAvailable() {
        return !!window.PacerPaceCore;
    }

    function getTargetElement(form) {
        var targetSelector = form.getAttribute('hx-target') || '#form-area';
        if (!targetSelector || targetSelector.charAt(0) !== '#') return form.parentElement;
        return document.querySelector(targetSelector) || form.parentElement;
    }

    function readFormInput(form) {
        var data = new FormData(form);
        var mode = data.get('mode') || 'auto';
        var input = { mode: mode, laenge: data.get('laenge') };

        if (mode === 'manuell') {
            input.bz_min = data.get('bz_min');
            input.bz_sec = data.get('bz_sec');
            input.ez_min = data.get('ez_min');
            input.ez_sec = data.get('ez_sec');
            input.hz_min = data.get('hz_min');
            input.hz_sec = data.get('hz_sec');
        } else {
            input.art = data.get('art');
            input.kmh = data.get('kmh');
        }

        return input;
    }

    function calculateFromForm(form) {
        var input = readFormInput(form);
        if (input.mode === 'manuell') {
            return window.PacerPaceCore.calculateManual(input);
        }
        return window.PacerPaceCore.calculateAuto(input);
    }

    function escapeHtml(value) {
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function formatArt(art) {
        if (!art) return '';
        if (art === 'wegstrecke') return 'Wegstrecke';
        if (art === 'hindernisstrecke') return 'Hindernisstrecke';
        if (art === 'schrittstrecke') return 'Schrittstrecke';
        return art;
    }

    function time(result, key) {
        return window.PacerPaceCore.formatTime(result[key]);
    }

    function renderDesktopRows(result, keys) {
        var hasBestzeit = !!result.bz_result;
        return keys.map(function(key) {
            return '<tr class="hover:bg-surface-overlay/30 transition-colors">' +
                '<td class="px-5 py-3.5 text-text-secondary font-medium">' + escapeHtml(key) + '</td>' +
                (hasBestzeit ? '<td class="px-5 py-3.5 text-center"><span class="time-bz font-mono font-bold text-lg">' + time(result.bz_result, key) + '</span></td>' : '') +
                '<td class="px-5 py-3.5 text-center"><span class="time-ez font-mono font-bold text-lg">' + time(result.ez_result, key) + '</span></td>' +
                '<td class="px-5 py-3.5 text-center"><span class="time-hz font-mono font-bold text-lg">' + time(result.hz_result, key) + '</span></td>' +
                '</tr>';
        }).join('');
    }

    function renderMobileCards(result, keys) {
        var hasBestzeit = !!result.bz_result;
        return keys.map(function(key) {
            return '<div class="card p-4">' +
                '<div class="text-text-muted text-sm font-semibold mb-2">' + escapeHtml(key) + ' m</div>' +
                '<div class="grid ' + (hasBestzeit ? 'grid-cols-3' : 'grid-cols-2') + ' gap-2">' +
                (hasBestzeit ? '<div class="bg-time-bz/10 border border-time-bz/20 rounded-xl p-2.5 text-center"><div class="text-time-bz text-xs font-semibold mb-1">BZ</div><div class="time-bz font-mono font-bold">' + time(result.bz_result, key) + '</div></div>' : '') +
                '<div class="bg-time-ez/10 border border-time-ez/20 rounded-xl p-2.5 text-center"><div class="text-time-ez text-xs font-semibold mb-1">EZ</div><div class="time-ez font-mono font-bold">' + time(result.ez_result, key) + '</div></div>' +
                '<div class="bg-time-hz/10 border border-time-hz/20 rounded-xl p-2.5 text-center"><div class="text-time-hz text-xs font-semibold mb-1">HZ</div><div class="time-hz font-mono font-bold">' + time(result.hz_result, key) + '</div></div>' +
                '</div></div>';
        }).join('');
    }

    function renderClientResult(result, isOnline) {
        var keys = Object.keys(result.ez_result);
        var hasBestzeit = !!result.bz_result;
        var statusTitle = isOnline ? 'Sofort berechnet' : 'Offline';
        var statusText = isOnline
            ? 'Die Berechnung wurde direkt auf diesem Gerät angezeigt. PDF-Link und Speicherung werden im Hintergrund vorbereitet.'
            : 'Die Berechnung wurde direkt auf diesem Gerät ausgeführt. PDF-Export, Speichern und Statistik sind wieder verfügbar, sobald Internet vorhanden ist.';
        return '<div class="animate-slide-up" data-offline-result>' +
            '<div class="card mb-6 border-l-4 border-l-yellow-500">' +
                '<div class="flex items-start gap-3">' +
                    '<div class="text-yellow-400 font-bold">' + statusTitle + '</div>' +
                    '<div class="text-text-secondary text-sm" data-save-status>' + statusText + '</div>' +
                '</div>' +
            '</div>' +
            '<div class="card mb-6"><div class="flex flex-wrap gap-6 justify-center md:justify-start">' +
                '<div><span class="text-text-muted text-xs uppercase tracking-wide block">Strecke</span><span class="text-text-primary font-bold text-2xl">' + escapeHtml(result.laenge) + '<span class="text-text-muted text-base font-normal ml-1">m</span></span></div>' +
                (result.kmh ? '<div><span class="text-text-muted text-xs uppercase tracking-wide block">Tempo</span><span class="text-text-primary font-bold text-2xl">' + escapeHtml(result.kmh) + '<span class="text-text-muted text-base font-normal ml-1">km/h</span></span></div>' : '') +
                (result.art ? '<div><span class="text-text-muted text-xs uppercase tracking-wide block">Streckenart</span><span class="text-text-primary font-bold text-2xl">' + escapeHtml(formatArt(result.art)) + '</span></div>' : '') +
            '</div></div>' +
            '<div class="hidden md:block"><div class="card overflow-hidden p-0"><table class="w-full"><thead><tr class="bg-surface-overlay/50">' +
                '<th class="px-5 py-3.5 text-left text-text-muted text-xs font-semibold uppercase tracking-wide">Strecke (m)</th>' +
                (hasBestzeit ? '<th class="px-5 py-3.5 text-center text-xs font-semibold uppercase tracking-wide"><span class="time-bz">Bestzeit</span></th>' : '') +
                '<th class="px-5 py-3.5 text-center text-xs font-semibold uppercase tracking-wide"><span class="time-ez">Erlaubte Zeit</span></th>' +
                '<th class="px-5 py-3.5 text-center text-xs font-semibold uppercase tracking-wide"><span class="time-hz">Höchstzeit</span></th>' +
            '</tr></thead><tbody class="divide-y divide-surface-border/50">' + renderDesktopRows(result, keys) + '</tbody></table></div></div>' +
            '<div class="md:hidden space-y-3">' + renderMobileCards(result, keys) + '</div>' +
            '<div class="mt-8"><div class="accent-bar mb-6"></div><div class="flex flex-wrap gap-3 justify-center" data-result-actions>' +
                '<button type="button" class="btn-primary inline-flex items-center gap-2" onclick="window.print()">Drucken / als PDF speichern</button>' +
                '<button type="button" class="btn-secondary inline-flex items-center gap-2" data-reset-offline-form>Neue Berechnung</button>' +
            '</div></div>' +
        '</div>';
    }

    function saveCalculationInBackground(form, target) {
        var status = target.querySelector('[data-save-status]');
        var actions = target.querySelector('[data-result-actions]');
        fetch('/api/calculations', {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'Accept': 'application/json'
            }
        }).then(function(response) {
            if (!response.ok) throw new Error('Speichern nicht möglich');
            return response.json();
        }).then(function(payload) {
            if (status) {
                status.textContent = 'Online gespeichert. Der serverseitige PDF-Export ist jetzt verfügbar.';
            }
            if (actions && payload.pdf_url && !actions.querySelector('[data-server-pdf-link]')) {
                actions.insertAdjacentHTML('afterbegin', '<a href="' + escapeHtml(payload.pdf_url) + '" class="btn-primary inline-flex items-center gap-2" data-server-pdf-link>PDF herunterladen</a>');
            }
        }).catch(function() {
            if (status) {
                status.textContent = 'Berechnung angezeigt, aber Speichern/PDF ist gerade nicht erreichbar. Drucken funktioniert weiterhin.';
            }
        });
    }

    document.addEventListener('submit', function(e) {
        var form = e.target;
        if (!form || !form.classList || !form.classList.contains('form-calculator')) return;
        if (!isClientCalculationAvailable()) return;

        e.preventDefault();
        e.stopImmediatePropagation();

        var target = getTargetElement(form);
        try {
            var isOnline = navigator.onLine !== false;
            var originalFormHtml = form.outerHTML;
            var result = calculateFromForm(form);
            target.innerHTML = renderClientResult(result, isOnline);
            target.dataset.offlineOriginalForm = originalFormHtml;
            if (isOnline) {
                saveCalculationInBackground(form, target);
            }
        } catch (err) {
            var error = form.querySelector('[data-laenge-error]');
            if (error) {
                error.textContent = err.message || 'Die Eingaben konnten nicht berechnet werden.';
                error.classList.remove('hidden');
            } else {
                alert(err.message || 'Die Eingaben konnten nicht berechnet werden.');
            }
        }
    }, true);

    document.addEventListener('click', function(e) {
        var button = e.target.closest('[data-reset-offline-form]');
        if (!button) return;
        var container = button.closest('[data-offline-result]');
        var target = container ? container.parentElement : document.getElementById('form-area');
        if (!target || !target.dataset.offlineOriginalForm) return;
        target.innerHTML = target.dataset.offlineOriginalForm;
        initializeSelectedArt(target);
    });
}());
