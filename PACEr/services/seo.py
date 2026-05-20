import json

DEFAULT_TITLE = 'PACEr - Fahrsport Marathon Zeitrechner'
DEFAULT_DESCRIPTION = (
    'PACEr berechnet Splitzeiten fuer den Fahrsport-Marathon: '
    'Bestzeit, erlaubte Zeit, Hoechstzeit und Kilometer-Splits auf einen Blick.'
)


def page_meta(title=None, description=None, canonical_path=None, robots=None):
    meta = {
        'meta_title': title or DEFAULT_TITLE,
        'meta_description': description or DEFAULT_DESCRIPTION,
        'canonical_path': canonical_path,
    }
    if robots:
        meta['meta_robots'] = robots
    return meta


def webapp_schema(base_url):
    base_url = base_url.rstrip('/')
    data = {
        '@context': 'https://schema.org',
        '@type': 'WebApplication',
        'name': 'PACEr',
        'applicationCategory': 'SportsApplication',
        'operatingSystem': 'Any',
        'url': base_url + '/',
        'description': DEFAULT_DESCRIPTION,
        'offers': {
            '@type': 'Offer',
            'price': '0',
            'priceCurrency': 'EUR',
        },
        'author': {
            '@type': 'Person',
            'name': 'Janneck Lehmann',
        },
    }
    return json.dumps(data, ensure_ascii=False)
