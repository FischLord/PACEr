import time
from collections import defaultdict

# In-memory store: ip -> list of failed attempt timestamps
_attempts = defaultdict(list)

MAX_ATTEMPTS = 5
WINDOW_SECONDS = 300  # 5 minutes


def _cleanup(ip):
    """Remove attempts older than the window."""
    cutoff = time.time() - WINDOW_SECONDS
    _attempts[ip] = [t for t in _attempts[ip] if t > cutoff]


def check_rate_limit(ip):
    """Return True if the IP is rate-limited (too many failed attempts)."""
    _cleanup(ip)
    return len(_attempts[ip]) >= MAX_ATTEMPTS


def record_attempt(ip):
    """Record a failed login attempt for the given IP."""
    _cleanup(ip)
    _attempts[ip].append(time.time())
