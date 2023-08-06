"""The *.manhuagui.com analyzer.

[Entry examples]

    - http://tw.manhuagui.com/comic/23292/
    - https://www.manhuagui.com/comic/23292/



[Preferences Description]

    ## meta_source

    Choice the one of the following as metadata source:

    - <tw.manhuagui.com> (tw) or
    - <www.manhuagui.com> (cn)



    ## image_host_codes

    Select which images servers should be used.

    Current available servers: ['eu', 'i', 'us']

    > Hint: The real servers url are look like this:
            `https://{image_host_code}.hamreus.com`
"""

import re

from cmdlr.exception import AnalyzerRuntimeError
from cmdlr.analyzer import BaseAnalyzer

from cmdlr.autil import fetch
from cmdlr.autil import get_random_useragent

from .infoext import extract_volumes
from .infoext import extract_name
from .infoext import extract_finished
from .infoext import extract_description
from .infoext import extract_authors
from .imgext import get_image_urls


class Analyzer(BaseAnalyzer):
    """Manhuagui analyzer."""

    entry_patterns = [
        re.compile(
            r'^https?://(www|tw).(?:manhuagui|ikanman).com/comic/(\d+)/?$',
        ),
    ]

    default_pref = {
        'image_host_codes': ['eu', 'i', 'us'],
        'meta_source': 'tw',
    }

    @property
    def default_request_kwargs(self):
        """Build default request kwargs."""
        return {
            'method': 'GET',
            'headers': {
                'referer': 'http://www.manhuagui.com/comic/',
                'user-agent': self.config['user_agent'],
            },
        }

    @staticmethod
    def to_config(pref):
        """Pre-build config."""
        def get_entry_subdomain(pref):
            meta_source = pref['meta_source']

            if meta_source == 'tw':
                entry_subdomain = 'tw'

            elif meta_source == 'cn':
                entry_subdomain = 'www'

            else:
                raise AnalyzerRuntimeError(
                    'manhuagui.meta_source should be one of'
                    ' ["tw", "cn", null]'
                )

            return entry_subdomain

        return {
            'image_host_codes': pref['image_host_codes'],
            'entry_subdomain': get_entry_subdomain(pref),
            'user_agent': get_random_useragent(),
        }

    def entry_normalizer(self, url):
        """Normalize all possible entry url to single one form."""
        match = self.entry_patterns[0].search(url)

        comic_id = match.group(2)
        origin_subdomain = match.group(1)

        conf_subdomain = self.config.get('entry_subdomain')
        subdomain = (origin_subdomain if conf_subdomain is None
                     else conf_subdomain)

        return 'https://{}.manhuagui.com/comic/{}/'.format(subdomain, comic_id)

    async def get_comic_info(self, url, request, loop):
        """Find comic info from entry."""
        fetch_result = await fetch(url, request)

        return {
            'name': extract_name(fetch_result),
            'volumes': await extract_volumes(fetch_result, loop),
            'description': extract_description(fetch_result),
            'authors': extract_authors(fetch_result),
            'finished': extract_finished(fetch_result),
        }

    async def save_volume_images(self, url, request, save_image, loop):
        """Get all images in one volume."""
        soup, _ = await fetch(url, request)

        image_host_codes = self.config.get('image_host_codes')

        image_urls = await get_image_urls(soup, image_host_codes, loop)

        for page_num, img_url in enumerate(image_urls, start=1):
            save_image(page_num, url=img_url)
