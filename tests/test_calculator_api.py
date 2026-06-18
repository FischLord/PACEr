import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = PROJECT_ROOT / 'PACEr'
sys.path.insert(0, str(APP_ROOT))

from app import create_app
from models import Calculation, db


class CalculatorApiTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        db_path = Path(self.tmpdir.name) / 'test-pacer.db'
        self.app = create_app({
            'TESTING': True,
            'SERVER_NAME': 'pacer.test',
            'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.tmpdir.cleanup()

    def csrf_token(self):
        response = self.client.get('/rechner')
        html = response.get_data(as_text=True)
        marker = 'name="_csrf_token" value="'
        start = html.index(marker) + len(marker)
        end = html.index('"', start)
        return html[start:end]

    def test_json_calculation_endpoint_saves_and_returns_pdf_url(self):
        response = self.client.post('/api/calculations', data={
            '_csrf_token': self.csrf_token(),
            'mode': 'auto',
            'laenge': '4900',
            'art': 'wegstrecke',
            'kmh': '13',
        })

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload['calculation_id'], 1)
        self.assertEqual(payload['pdf_url'], '/api/export/pdf/1')
        self.assertIsNotNone(payload['followup_form_url'])

        with self.app.app_context():
            calc = db.session.get(Calculation, 1)
            self.assertIsNotNone(calc)
            self.assertEqual(calc.laenge, 4900)
            self.assertEqual(calc.art, 'wegstrecke')
            self.assertEqual(calc.kmh, 13)

    def test_json_calculation_endpoint_validates_csrf(self):
        response = self.client.post('/api/calculations', data={
            'mode': 'auto',
            'laenge': '4900',
            'art': 'wegstrecke',
            'kmh': '13',
        })

        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
