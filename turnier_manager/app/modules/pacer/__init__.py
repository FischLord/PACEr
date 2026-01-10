"""
PACEr Module - Pace Calculator
"""
from flask import Blueprint

bp = Blueprint('pacer', __name__)

from . import routes  # noqa
