const assert = require('assert');
const paceCore = require('../../PACEr/static/js/pace-core');

function assertAutoCase(input, expected) {
    const result = paceCore.calculateAuto(input);
    assert.deepStrictEqual(result.times, expected.times);
    assert.deepStrictEqual(result.ez_result, expected.ez_result);
    assert.deepStrictEqual(result.hz_result, expected.hz_result);
    assert.deepStrictEqual(result.bz_result, expected.bz_result);
}

assertAutoCase(
    { laenge: 4900, kmh: 13, art: 'wegstrecke' },
    {
        times: { bz_sec: 36, hz_sec: 7, ez_sec: 36, bz_min: 20, hz_min: 27, ez_min: 22 },
        ez_result: {
            1000: { min: 4, sec: 36 },
            2000: { min: 9, sec: 13 },
            3000: { min: 13, sec: 50 },
            4000: { min: 18, sec: 26 },
            4900: { min: 22, sec: 36 }
        },
        hz_result: {
            1000: { min: 5, sec: 32 },
            2000: { min: 11, sec: 4 },
            3000: { min: 16, sec: 36 },
            4000: { min: 22, sec: 8 },
            4900: { min: 27, sec: 7 }
        },
        bz_result: {
            1000: { min: 4, sec: 12 },
            2000: { min: 8, sec: 24 },
            3000: { min: 12, sec: 36 },
            4000: { min: 16, sec: 48 },
            4900: { min: 20, sec: 36 }
        }
    }
);

assertAutoCase(
    { laenge: 5000, kmh: 12, art: 'hindernisstrecke' },
    {
        times: { bz_sec: 0, hz_sec: 0, ez_sec: 0, bz_min: 22, hz_min: 50, ez_min: 25 },
        ez_result: {
            1000: { min: 5, sec: 0 },
            2000: { min: 10, sec: 0 },
            3000: { min: 15, sec: 0 },
            4000: { min: 20, sec: 0 },
            5000: { min: 25, sec: 0 }
        },
        hz_result: {
            1000: { min: 10, sec: 0 },
            2000: { min: 20, sec: 0 },
            3000: { min: 30, sec: 0 },
            4000: { min: 40, sec: 0 },
            5000: { min: 50, sec: 0 }
        },
        bz_result: {
            1000: { min: 4, sec: 24 },
            2000: { min: 8, sec: 48 },
            3000: { min: 13, sec: 12 },
            4000: { min: 17, sec: 36 },
            5000: { min: 22, sec: 0 }
        }
    }
);

assertAutoCase(
    { laenge: 1000, kmh: 6, art: 'schrittstrecke' },
    {
        times: { bz_sec: null, hz_sec: 0, ez_sec: 0, bz_min: null, hz_min: 20, ez_min: 10 },
        ez_result: { 1000: { min: 10, sec: 0 } },
        hz_result: { 1000: { min: 20, sec: 0 } },
        bz_result: null
    }
);

assertAutoCase(
    { laenge: 999, kmh: 10, art: 'wegstrecke' },
    {
        times: { bz_sec: 59, hz_sec: 10, ez_sec: 59, bz_min: 3, hz_min: 7, ez_min: 5 },
        ez_result: { 999: { min: 5, sec: 59 } },
        hz_result: { 999: { min: 7, sec: 10 } },
        bz_result: { 999: { min: 3, sec: 59 } }
    }
);

assert.deepStrictEqual(
    paceCore.calculateManual({ laenge: 4900, bz_min: 20, bz_sec: 36, ez_min: 22, ez_sec: 36, hz_min: 27, hz_sec: 7 }),
    {
        laenge: 4900,
        kmh: null,
        art: null,
        ez_result: {
            1000: { min: 4, sec: 36 },
            2000: { min: 9, sec: 13 },
            3000: { min: 13, sec: 50 },
            4000: { min: 18, sec: 26 },
            4900: { min: 22, sec: 36 }
        },
        hz_result: {
            1000: { min: 5, sec: 32 },
            2000: { min: 11, sec: 4 },
            3000: { min: 16, sec: 36 },
            4000: { min: 22, sec: 8 },
            4900: { min: 27, sec: 7 }
        },
        bz_result: {
            1000: { min: 4, sec: 12 },
            2000: { min: 8, sec: 24 },
            3000: { min: 12, sec: 36 },
            4000: { min: 16, sec: 48 },
            4900: { min: 20, sec: 36 }
        },
        times: { bz_sec: 36, hz_sec: 7, ez_sec: 36, bz_min: 20, hz_min: 27, ez_min: 22 }
    }
);

assert.strictEqual(paceCore.formatTime({ min: 4, sec: 5 }), '4:05');
assert.throws(() => paceCore.calculateAuto({ laenge: 0, kmh: 10, art: 'wegstrecke' }), /Streckenlaenge/);
assert.throws(() => paceCore.calculateAuto({ laenge: 100001, kmh: 10, art: 'wegstrecke' }), /Streckenlaenge/);
assert.throws(() => paceCore.calculateAuto({ laenge: 1000, kmh: 10, art: 'unbekannt' }), /Art not defined/);
assert.throws(() => paceCore.calculateManual({ laenge: 1000, bz_min: 1, bz_sec: 60, ez_min: 2, ez_sec: 0, hz_min: 3, hz_sec: 0 }), /Sekunden/);

console.log('pace-core tests passed');
