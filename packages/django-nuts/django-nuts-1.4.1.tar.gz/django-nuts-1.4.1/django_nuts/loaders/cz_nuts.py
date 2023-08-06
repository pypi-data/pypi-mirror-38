import logging
import os

import lxml.html

from . import urlopen
from ..models import NUTS

logger = logging.getLogger(__name__)

CZ_NUTS_URL = os.environ.get(
    'CZ_NUTS_URL',
    'http://www.risy.cz/cs/administrativni-cleneni-nuts-cesko',
)


def load_cz_nuts():
    with urlopen(CZ_NUTS_URL) as response:
        content = response.read()
    tree = lxml.html.fromstring(content)
    found, created, updated = 0, 0, 0
    nuts = {n.code: n for n in NUTS.objects.filter(code__startswith='CZ').iterator()}
    for tr in tree.xpath('//table[contains(@class, "blue")]//tr'):
        row = [td.text_content().strip() for td in tr.findall('td')]
        try:
            code = row[0]
            level = len(code) - 2
            name = row[level + 1]
            if name == 'Extra-Regio':
                continue
        except IndexError:
            continue
        else:
            found += 1
            logger.debug('Found %s %s', code, name)
        if code not in nuts:
            nuts[code] = NUTS.objects.create(
                code=code,
                name=name,
                level=level,
            )
            created += 1
        elif nuts[code].name != name:
            nuts[code].name = name
            nuts[code].save()
            updated += 1
    logger.info('Found %d NUTS, %d created, %d updated.', found, created, updated)
