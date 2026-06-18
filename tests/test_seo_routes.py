import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = PROJECT_ROOT / 'PACEr'
sys.path.insert(0, str(APP_ROOT))

from app import create_app


class SeoRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        db_path = Path(self.tmpdir.name) / 'test-pacer.db'
        self.app = create_app({
            'TESTING': True,
            'SERVER_NAME': 'pacer.test',
            'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
            'WTF_CSRF_ENABLED': False,
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_home_has_canonical_meta_and_structured_data(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('<title>PACEr - Fahrsport Marathon Zeitrechner</title>', html)
        self.assertIn('<meta name="description"', html)
        self.assertIn('<meta name="robots" content="index,follow" />', html)
        self.assertIn('<link rel="canonical" href="http://pacer.test/" />', html)
        self.assertIn('"@type": "WebApplication"', html)

    def test_projekt_info_uses_home_canonical_to_avoid_duplicate_content(self):
        response = self.client.get('/projektInfo')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('<link rel="canonical" href="http://pacer.test/" />', html)

    def test_admin_login_is_noindex(self):
        response = self.client.get('/adminLogin')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('<meta name="robots" content="noindex,nofollow" />', html)

    def test_robots_txt_references_sitemap_and_blocks_admin_pages(self):
        response = self.client.get('/robots.txt')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'text/plain')
        body = response.get_data(as_text=True)
        self.assertIn('Disallow: /admin', body)
        self.assertIn('Disallow: /adminLogin', body)
        self.assertIn('Sitemap: http://pacer.test/sitemap.xml', body)

    def test_sitemap_contains_public_routes_only(self):
        response = self.client.get('/sitemap.xml')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'application/xml')
        body = response.get_data(as_text=True)
        self.assertIn('<loc>http://pacer.test/</loc>', body)
        self.assertIn('<loc>http://pacer.test/rechner</loc>', body)
        self.assertIn('<loc>http://pacer.test/turniere</loc>', body)
        self.assertIn('<loc>http://pacer.test/reportProblem</loc>', body)
        self.assertNotIn('/admin', body)
        self.assertNotIn('/adminLogin', body)
    def test_calculator_loads_pace_core_before_calculator_script(self):
        response = self.client.get('/rechner')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        pace_core_index = html.index('/static/js/pace-core.js')
        calculator_index = html.index('/static/js/calculator.js')
        self.assertLess(pace_core_index, calculator_index)
    def test_layout_links_manifest_and_registers_service_worker(self):
        response = self.client.get('/rechner')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('/static/manifest.webmanifest', html)
        self.assertIn("navigator.serviceWorker.register('/sw.js')", html)

    def test_service_worker_is_served_from_root_scope(self):
        response = self.client.get('/sw.js')

        self.assertEqual(response.status_code, 200)
        self.assertIn(response.mimetype, ['application/javascript', 'text/javascript'])
        self.assertEqual(response.headers.get('Service-Worker-Allowed'), '/')
        self.assertEqual(response.headers.get('Cache-Control'), 'no-cache')
        self.assertIn('pacer-offline-v1', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
