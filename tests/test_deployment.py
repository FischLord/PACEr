import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import request
from sqlalchemy import event
from werkzeug.security import check_password_hash

APP_ROOT = Path(__file__).resolve().parents[1] / 'PACEr'
sys.path.insert(0, str(APP_ROOT))

from app import create_app
from models import User, db


class DeploymentTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.config = {
            'TESTING': True,
            'SECRET_KEY': 'deployment-test-session-key',
            'SQLALCHEMY_DATABASE_URI': f'sqlite:///{self.tmpdir.name}/pacer.db',
        }
        self.env = patch.dict(os.environ, {
            'ADMIN_PASSWORD': '',
            'SESSION_COOKIE_SECURE': 'true',
            'PROXY_FIX_X_FOR': '2',
            'PROXY_FIX_X_PROTO': '1',
            'PROXY_FIX_X_HOST': '1',
        })
        self.env.start()
        self.addCleanup(self.env.stop)

    def make_app(self, **config):
        app = create_app({**self.config, **config})

        def dispose():
            with app.app_context():
                db.session.remove()
                db.engine.dispose()

        self.addCleanup(dispose)
        return app

    def test_health_without_login_cookie_or_database_queries(self):
        app = self.make_app()

        def reject_query(*args):
            raise AssertionError('Healthcheck darf keine Datenbankabfrage ausführen')

        with app.app_context():
            event.listen(db.engine, 'before_cursor_execute', reject_query)
            response = app.test_client().get('/healthz')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'ok\n')
        self.assertNotIn('Set-Cookie', response.headers)

    def test_proxy_headers_produce_https_urls_and_client_ip(self):
        app = self.make_app()

        @app.get('/test-client-ip')
        def client_ip():
            return request.remote_addr

        client = app.test_client()
        headers = {
            'X-Forwarded-For': 'spoofed, 198.51.100.10, 172.18.0.2',
            'X-Forwarded-Proto': 'https',
            'X-Forwarded-Host': 'pacer.apps.j-rz.de',
        }
        response = client.get('/robots.txt', headers=headers)
        self.assertIn('Sitemap: https://pacer.apps.j-rz.de/sitemap.xml', response.text)
        self.assertEqual(client.get('/test-client-ip', headers=headers).text, '198.51.100.10')
        headers['X-Forwarded-Host'] = 'pacer-pr42.preview.j-rz.de'
        self.assertIn('https://pacer-pr42.preview.j-rz.de/sitemap.xml',
                      client.get('/robots.txt', headers=headers).text)

    def test_single_proxy_and_disabled_proxy_trust(self):
        for count, expected in [(1, 'https://public.test'), (0, 'http://localhost')]:
            with self.subTest(count=count), patch.dict(os.environ, {
                'PROXY_FIX_X_FOR': str(count),
                'PROXY_FIX_X_PROTO': str(count),
                'PROXY_FIX_X_HOST': str(count),
            }):
                app = self.make_app()
                response = app.test_client().get('/robots.txt', headers={
                    'X-Forwarded-For': '198.51.100.10',
                    'X-Forwarded-Proto': 'https',
                    'X-Forwarded-Host': 'public.test',
                })
                self.assertIn(f'Sitemap: {expected}/sitemap.xml', response.text)

    def test_secure_session_cookie_can_be_enabled_and_disabled(self):
        for value, secure in [('true', True), ('false', False)]:
            with self.subTest(value=value), patch.dict(os.environ, {'SESSION_COOKIE_SECURE': value}):
                app = self.make_app()
                response = app.test_client().get('/adminLogin')
                cookie = response.headers['Set-Cookie']
                self.assertEqual('Secure;' in cookie, secure)
                self.assertIn('HttpOnly;', cookie)
                self.assertIn('SameSite=Lax', cookie)

    def test_missing_or_empty_admin_password_does_not_seed_admin(self):
        for password in [None, '']:
            with self.subTest(password=password):
                if password is None:
                    os.environ.pop('ADMIN_PASSWORD', None)
                else:
                    os.environ['ADMIN_PASSWORD'] = password
                app = self.make_app()
                with app.app_context():
                    self.assertIsNone(User.query.filter_by(username='admin').first())

    def test_admin_can_login_and_existing_password_survives_restart(self):
        password = 'deployment-test-admin-password'
        with patch.dict(os.environ, {'ADMIN_PASSWORD': password}):
            app = self.make_app()
        client = app.test_client()
        with client.session_transaction() as session:
            session['_csrf_token'] = 'test-token'
        response = client.post('/adminLogin', base_url='https://localhost', data={
            '_csrf_token': 'test-token', 'username': 'admin', 'password': password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(client.get('/adminTools', base_url='https://localhost').status_code, 200)
        with app.app_context():
            original_hash = User.query.filter_by(username='admin').one().password_hash

        for replacement in ['', 'another-test-password']:
            with self.subTest(replacement=replacement), patch.dict(os.environ, {'ADMIN_PASSWORD': replacement}):
                restarted_app = self.make_app()
                with restarted_app.app_context():
                    admin = User.query.filter_by(username='admin').one()
                    self.assertEqual(admin.password_hash, original_hash)
                    self.assertTrue(check_password_hash(admin.password_hash, password))


if __name__ == '__main__':
    unittest.main()
