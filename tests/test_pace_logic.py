import sys
import unittest
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1] / 'PACEr'
sys.path.insert(0, str(APP_ROOT))

from helper import calculatePace, pace


class PaceLogicTestCase(unittest.TestCase):
    def assert_auto_case(self, laenge, kmh, art, expected_times, expected_ez, expected_hz, expected_bz):
        bz_sec, hz_sec, ez_sec, bz_min, hz_min, ez_min = calculatePace(laenge, kmh, art)
        self.assertEqual(
            {
                'bz_sec': bz_sec,
                'hz_sec': hz_sec,
                'ez_sec': ez_sec,
                'bz_min': bz_min,
                'hz_min': hz_min,
                'ez_min': ez_min,
            },
            expected_times,
        )
        self.assertEqual(pace(laenge, ez_min, ez_sec), expected_ez)
        self.assertEqual(pace(laenge, hz_min, hz_sec), expected_hz)
        if expected_bz is None:
            self.assertIsNone(bz_min)
            self.assertIsNone(bz_sec)
        else:
            self.assertEqual(pace(laenge, bz_min, bz_sec), expected_bz)

    def test_wegstrecke_with_restmeters_matches_current_rounding(self):
        self.assert_auto_case(
            4900,
            13,
            'wegstrecke',
            {'bz_sec': 36, 'hz_sec': 7, 'ez_sec': 36, 'bz_min': 20, 'hz_min': 27, 'ez_min': 22},
            {
                1000: {'min': 4, 'sec': 36},
                2000: {'min': 9, 'sec': 13},
                3000: {'min': 13, 'sec': 50},
                4000: {'min': 18, 'sec': 26},
                4900: {'min': 22, 'sec': 36},
            },
            {
                1000: {'min': 5, 'sec': 32},
                2000: {'min': 11, 'sec': 4},
                3000: {'min': 16, 'sec': 36},
                4000: {'min': 22, 'sec': 8},
                4900: {'min': 27, 'sec': 7},
            },
            {
                1000: {'min': 4, 'sec': 12},
                2000: {'min': 8, 'sec': 24},
                3000: {'min': 12, 'sec': 36},
                4000: {'min': 16, 'sec': 48},
                4900: {'min': 20, 'sec': 36},
            },
        )

    def test_hindernisstrecke_exact_kilometers(self):
        self.assert_auto_case(
            5000,
            12,
            'hindernisstrecke',
            {'bz_sec': 0, 'hz_sec': 0, 'ez_sec': 0, 'bz_min': 22, 'hz_min': 50, 'ez_min': 25},
            {1000: {'min': 5, 'sec': 0}, 2000: {'min': 10, 'sec': 0}, 3000: {'min': 15, 'sec': 0}, 4000: {'min': 20, 'sec': 0}, 5000: {'min': 25, 'sec': 0}},
            {1000: {'min': 10, 'sec': 0}, 2000: {'min': 20, 'sec': 0}, 3000: {'min': 30, 'sec': 0}, 4000: {'min': 40, 'sec': 0}, 5000: {'min': 50, 'sec': 0}},
            {1000: {'min': 4, 'sec': 24}, 2000: {'min': 8, 'sec': 48}, 3000: {'min': 13, 'sec': 12}, 4000: {'min': 17, 'sec': 36}, 5000: {'min': 22, 'sec': 0}},
        )

    def test_schrittstrecke_has_no_bestzeit(self):
        self.assert_auto_case(
            1000,
            6,
            'schrittstrecke',
            {'bz_sec': None, 'hz_sec': 0, 'ez_sec': 0, 'bz_min': None, 'hz_min': 20, 'ez_min': 10},
            {1000: {'min': 10, 'sec': 0}},
            {1000: {'min': 20, 'sec': 0}},
            None,
        )

    def test_under_one_kilometer_only_contains_finish_distance(self):
        self.assert_auto_case(
            999,
            10,
            'wegstrecke',
            {'bz_sec': 59, 'hz_sec': 10, 'ez_sec': 59, 'bz_min': 3, 'hz_min': 7, 'ez_min': 5},
            {999: {'min': 5, 'sec': 59}},
            {999: {'min': 7, 'sec': 10}},
            {999: {'min': 3, 'sec': 59}},
        )

    def test_manual_pace_keeps_finish_time_and_splits(self):
        self.assertEqual(
            pace(4900, 22, 36),
            {
                1000: {'min': 4, 'sec': 36},
                2000: {'min': 9, 'sec': 13},
                3000: {'min': 13, 'sec': 50},
                4000: {'min': 18, 'sec': 26},
                4900: {'min': 22, 'sec': 36},
            },
        )


if __name__ == '__main__':
    unittest.main()
