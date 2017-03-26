import re
import logging
import requests
from datetime import date
from lxml import html
from lxml.etree import tostring
from django.utils.timezone import now
from . import BaseExtractor
from ..models import POTD
logger = logging.getLogger('management')


class WikipediaEnExtractor(BaseExtractor):
    """Extractor for the english Wikipedia"""
    WIKIPEDIA_BASE_URL = r'https://en.wikipedia.org'
    WIKIPEDIA_POTD_URL = r'https://en.wikipedia.org/wiki/Template:POTD/{year:0>4}-{month:0>2}-{day:0>2}'
    WIKIPEDIA_API_URL = r'https://en.wikipedia.org/w/api.php?action=query&titles=Template:POTD/{year:0>4}-{month:0>2}-{day:0>2}&prop=revisions&rvprop=content&format=json'
    WIKIMEDIA_COMMONS_URL = r'https://tools.wmflabs.org/magnus-toolserver/commonsapi.php?image={image_filename}'
    WIKI_TEXT_IMAGE_RE = re.compile(r'.*\|\s*image\s*=\s*(?P<image_filename>[^\|]+)\|.*')
    WIKI_TEXT_TITLE_RE = re.compile(r'.*\[\[[^\|]+\|(?P<title>[^\]]+)\]\].*')

    def __init__(self):
        super().__init__()
        self.source_type = POTD.PICTURE_SOURCE_WIKIPEDIA_EN

    def extract(self, year, month, day, update_existing=False, max_thumb_size=None):
        max_thumb_size = max_thumb_size or self.max_thumb_size
        potd_kwargs = {'potd_at': date(year=year, month=month, day=day), 'source_type': self.source_type}
        try:
            potd = POTD.objects.get(**potd_kwargs)
            if not update_existing:
                logger.info('extractor wikipedia_en: potd already existing and not updating: {}'.format(potd))
                return
            else:
                logger.debug('extractor wikipedia_en: using already existing potd: {}'.format(potd_kwargs))
        except POTD.DoesNotExist:
            logger.debug('extractor wikipedia_en: creating new potd for {}'.format(potd_kwargs))
            potd = POTD(**potd_kwargs)

        source_potd_url = WikipediaEnExtractor.WIKIPEDIA_POTD_URL.format(year=year, month=month, day=day)
        logger.debug('extractor wikipedia_en: source potd url: {}'.format(source_potd_url))
        response = requests.get(source_potd_url)

        if response.ok:
            tree = html.fromstring(response.content)
            image_filename = tree.xpath('//div[@id="mw-content-text"][1]/table//img[1]/..')[0].attrib['href'].split(':')[1]
            potd.title = tree.xpath('//div[@id="mw-content-text"][1]/table//tr/td/p//b/a')[0].attrib['title']
            potd.source_url = WikipediaEnExtractor.WIKIPEDIA_BASE_URL + tree.xpath('//div[@id="mw-content-text"][1]/table//tr/td/p//b/a')[0].attrib['href']
            potd.description = tree.xpath('//div[@id="mw-content-text"][1]/table//tr/td/p//b/a/ancestor::p')[0].text_content()
        else:
            logger.error('extractor wikipedia_en: http status code {} for url: {}'.format(
                response.status_code, source_potd_url))
            response.raise_for_status()

        # Wikimedia Commons
        source_image_api_url = WikipediaEnExtractor.WIKIMEDIA_COMMONS_URL.format(image_filename=image_filename)
        if max_thumb_size:
            source_image_api_url += r'&thumbwidth={0}&thumbheight={0}'.format(max_thumb_size)
        logger.debug('extractor wikipedia_en: source image api url: {}'.format(source_image_api_url))
        response = requests.get(source_image_api_url)

        if response.ok:
            tree = html.fromstring(response.content)
            potd.raw_scraping_data_image = tostring(tree, encoding='unicode', pretty_print=True)
            potd.image_url = tree.xpath('//urls/file')[0].text
            potd.image_thumbnail_url = None
            try:
                potd.image_thumbnail_url = tree.xpath('//urls/thumbnail')[0].text
            except (KeyError, IndexError):
                logger.debug('extractor wikipedia_en: image thumbnail url not found: {}'.format(source_image_api_url))
                pass
        else:
            logger.error('extractor wikipedia_en: wikimedia commons http status code {} for url: {}'.format(
                response.status_code, source_image_api_url))
            response.raise_for_status()

        potd.retrieved_from_source_at = now()

        logger.info('extractor wikipedia_en: potd_data okay for {}-{}-{} "{}"'.format(
            year, month, day, potd.title))

        potd.save()

        return potd
