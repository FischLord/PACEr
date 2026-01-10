"""
History Module - Public Calculation History
"""
from flask import Blueprint

bp = Blueprint('history', __name__)

from . import routes  # noqa
