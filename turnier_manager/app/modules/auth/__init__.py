"""
Auth Module - Admin Authentication (Hash-based)
"""
from flask import Blueprint

bp = Blueprint('auth', __name__)

from . import routes  # noqa
