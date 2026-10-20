import os

bind = '0.0.0.0:8000'
workers = int(os.environ.get('WEB_CONCURRENCY', '1'))
threads = int(os.environ.get('GUNICORN_THREADS', '4'))
worker_tmp_dir = '/data/tmp'
os.makedirs(worker_tmp_dir, exist_ok=True)
accesslog = '-'
errorlog = '-'

# ProxyFix handles the explicitly configured forwarded headers.
forwarded_allow_ips = ''
