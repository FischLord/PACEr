from datetime import date
import re

from flask import request, session

from models import db, ReferralStatistic

MAX_VALUE_LENGTH = 80
SAFE_VALUE = re.compile(r'[^a-zA-Z0-9_.-]+')


def clean_ref(value):
    if not value:
        return 'direkt'
    value = SAFE_VALUE.sub('-', value.strip())[:MAX_VALUE_LENGTH].strip('-')
    return value or 'direkt'


def current_ref():
    return clean_ref(
        request.args.get('ref')
        or request.args.get('utm_campaign')
        or request.args.get('utm_source')
        or session.get('ref')
    )


def capture_referral():
    value = (
        request.args.get('ref')
        or request.args.get('utm_campaign')
        or request.args.get('utm_source')
    )
    if value:
        session['ref'] = clean_ref(value)


def record_referral_event(event_type, path=None, ref=None):
    ref_value = clean_ref(ref) if ref is not None else current_ref()
    path_value = (path or request.path or '/')[:120]
    today = date.today()

    try:
        stat = ReferralStatistic.query.filter_by(
            date=today,
            event_type=event_type,
            ref=ref_value,
            path=path_value,
        ).first()

        if stat:
            stat.count += 1
        else:
            stat = ReferralStatistic(
                date=today,
                event_type=event_type,
                ref=ref_value,
                path=path_value,
                count=1,
            )
            db.session.add(stat)

        db.session.commit()
    except Exception:
        db.session.rollback()
