(function (root, factory) {
    if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.PacerPaceCore = factory();
    }
}(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    var MAX_LENGTH = 100000;
    var VALID_ARTEN = ['wegstrecke', 'hindernisstrecke', 'schrittstrecke'];
    var KMH_RANGES = {
        hindernisstrecke: { min: 8, max: 14 },
        wegstrecke: { min: 8, max: 15 },
        schrittstrecke: { min: 3, max: 7 }
    };

    function isIntegerString(value) {
        return /^-?\d+$/.test(String(value).trim());
    }

    function toInt(value, fieldName) {
        if (!isIntegerString(value)) {
            throw new Error((fieldName || 'Wert') + ' muss eine ganze Zahl sein.');
        }
        var number = Number(value);
        if (!Number.isFinite(number)) {
            throw new Error((fieldName || 'Wert') + ' muss eine Zahl sein.');
        }
        return Math.trunc(number);
    }

    function validateLength(laenge) {
        var length = toInt(laenge, 'Streckenlaenge');
        if (length <= 0 || length > MAX_LENGTH) {
            throw new Error('Bitte eine Streckenlaenge zwischen 1 und ' + MAX_LENGTH + ' m angeben.');
        }
        return length;
    }

    function validateNonNegativeMinutes(minutes, fieldName) {
        var value = toInt(minutes, fieldName || 'Minuten');
        if (value < 0) {
            throw new Error((fieldName || 'Minuten') + ' muessen mindestens 0 sein.');
        }
        return value;
    }

    function validateKmh(kmh, art) {
        var speed = toInt(kmh, 'Tempo');
        var range = KMH_RANGES[art];
        if (!range) {
            throw new Error('Error: Art not defined');
        }
        if (speed < range.min || speed > range.max) {
            throw new Error('Tempo muss fuer diese Streckenart zwischen ' + range.min + ' und ' + range.max + ' km/h liegen.');
        }
        return speed;
    }

    function validateSeconds(seconds, fieldName) {
        var value = toInt(seconds, fieldName || 'Sekunden');
        if (value < 0 || value > 59) {
            throw new Error((fieldName || 'Sekunden') + ' muessen zwischen 0 und 59 liegen.');
        }
        return value;
    }

    function pace(laenge, timeMin, timeSec) {
        var length = validateLength(laenge);
        var minutes = validateNonNegativeMinutes(timeMin, 'Minuten');
        var seconds = toInt(timeSec, 'Sekunden');
        var totalSeconds = minutes * 60 + seconds;
        var result = {};

        if (length >= 1000) {
            var pacePerKm = totalSeconds / length * 1000;
            for (var km = 1; km <= Math.trunc(length / 1000); km++) {
                var timeKm = km * pacePerKm;
                result[String(km * 1000)] = {
                    min: Math.trunc(timeKm / 60),
                    sec: Math.trunc(timeKm % 60)
                };
            }
        }

        result[String(length)] = { min: minutes, sec: seconds };
        return result;
    }

    function calculatePace(laenge, kmh, art) {
        var length = validateLength(laenge);
        if (VALID_ARTEN.indexOf(art) === -1) {
            throw new Error('Error: Art not defined');
        }
        var speed = validateKmh(kmh, art);

        var laengeKm = length / 1000;
        var ez = laengeKm * 60 / speed;
        ez = Math.trunc(ez * 60);

        var hz;
        var bz;
        if (art === 'wegstrecke') {
            hz = ez + (ez * 0.2);
            bz = ez - 120;
        } else if (art === 'hindernisstrecke') {
            hz = 2 * ez;
            bz = ez - 180;
        } else if (art === 'schrittstrecke') {
            hz = 2 * ez;
            bz = null;
        }

        var ezMin = Math.trunc(ez / 60);
        var ezSec = Math.trunc(ez % 60);
        var hzMin = Math.trunc(hz / 60);
        var hzSec = Math.trunc(hz % 60);
        var bzMin = null;
        var bzSec = null;
        if (bz !== null) {
            bzMin = Math.trunc(bz / 60);
            bzSec = Math.trunc(bz % 60);
        }

        return {
            bz_sec: bzSec,
            hz_sec: hzSec,
            ez_sec: ezSec,
            bz_min: bzMin,
            hz_min: hzMin,
            ez_min: ezMin
        };
    }

    function calculateAuto(input) {
        var calc = calculatePace(input.laenge, input.kmh, input.art);
        var result = {
            laenge: validateLength(input.laenge),
            kmh: validateKmh(input.kmh, input.art),
            art: input.art,
            ez_result: pace(input.laenge, calc.ez_min, calc.ez_sec),
            hz_result: pace(input.laenge, calc.hz_min, calc.hz_sec),
            bz_result: null,
            times: calc
        };

        if (calc.bz_min !== null) {
            result.bz_result = pace(input.laenge, calc.bz_min, calc.bz_sec);
        }

        return result;
    }

    function calculateManual(input) {
        var bzSec = validateSeconds(input.bz_sec, 'Bestzeit-Sekunden');
        var ezSec = validateSeconds(input.ez_sec, 'Erlaubte-Zeit-Sekunden');
        var hzSec = validateSeconds(input.hz_sec, 'Hoechstzeit-Sekunden');

        return {
            laenge: validateLength(input.laenge),
            kmh: null,
            art: null,
            ez_result: pace(input.laenge, input.ez_min, ezSec),
            hz_result: pace(input.laenge, input.hz_min, hzSec),
            bz_result: pace(input.laenge, input.bz_min, bzSec),
            times: {
                bz_sec: bzSec,
                hz_sec: hzSec,
                ez_sec: ezSec,
                bz_min: validateNonNegativeMinutes(input.bz_min, 'Bestzeit-Minuten'),
                hz_min: validateNonNegativeMinutes(input.hz_min, 'Hoechstzeit-Minuten'),
                ez_min: validateNonNegativeMinutes(input.ez_min, 'Erlaubte-Zeit-Minuten')
            }
        };
    }

    function formatTime(time) {
        return String(time.min) + ':' + String(time.sec).padStart(2, '0');
    }

    return {
        MAX_LENGTH: MAX_LENGTH,
        pace: pace,
        calculatePace: calculatePace,
        calculateAuto: calculateAuto,
        calculateManual: calculateManual,
        formatTime: formatTime
    };
}));
