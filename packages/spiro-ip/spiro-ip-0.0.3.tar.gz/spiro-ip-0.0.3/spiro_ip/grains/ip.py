import requests
import random
import logging


def _get(url):
    with requests.Session() as s:
        resp = s.get(url, timeout=5)
        resp.raise_for_status()
        return resp


IP4_FINDERS = [
    # https://whatismyipaddress.com/api
    lambda: (_get('https://ipv4bot.whatismyipaddress.com/').text.strip()),
    # http://api.ident.me/
    lambda: (_get('https://v4.ident.me/').text.strip()),
    # https://seeip.org
    lambda: (_get('https://ip4.seeip.org/').text.strip()),
    # https://wtfismyip.com/
    lambda: (_get('https://ipv4.wtfismyip.com/text').text.strip()),
    # https://major.io/icanhazip-com-faq/
    lambda: (_get('https://ipv4.icanhazip.com/').text.strip()),
]

IP6_FINDERS = [
    # https://whatismyipaddress.com/api
    lambda: (_get('https://ipv6bot.whatismyipaddress.com/').text.strip()),
    # http://api.ident.me/
    lambda: (_get('https://v6.ident.me/').text.strip()),
    # https://seeip.org
    lambda: (_get('https://ip6.seeip.org/').text.strip()),
    # https://wtfismyip.com/
    lambda: (_get('https://ipv6.wtfismyip.com/text').text.strip()),
    # https://major.io/icanhazip-com-faq/
    lambda: (_get('https://ipv6.icanhazip.com/').text.strip()),
]


def _find_one(pile):
    log = logging.getLogger('ip.grains')
    for _ in range(5):
        req = random.choice(pile)
        log.debug('Attempting %r', req)
        try:
            return req() or ''
        except Exception as e:
            log.debug(e)
            continue
    return ''


def externalips():
    return {
        'externalip4': _find_one(IP4_FINDERS),
        'externalip6': _find_one(IP6_FINDERS),
    }
