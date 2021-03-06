import re
import logging
import requests
from datetime import date
from lxml import html
from lxml.etree import tostring
from django.utils.timezone import now
from django.conf import settings
from html2text import HTML2Text
from . import BaseExtractor
from ..models import POTD

logger = logging.getLogger('management.' + __name__)


class NASAAPODEnExtractor(BaseExtractor):
    """Extractor for the NASA APOD
    """
    APOD_BASE_URL = r'https://apod.nasa.gov/'
    APOD_DETAIL_URL_BY_DATE = r'https://apod.nasa.gov/apod/ap{yy}{mm:02d}{dd:02d}.html'
    UGLY_TAG_STRIP_RE = re.compile(r'<\s*/?\s*center\s*>|<\s*b[^>]*>(.*?)<\s*/\s*b>', re.DOTALL)

    def __init__(self):
        super().__init__()
        self.source_type = POTD.PICTURE_SOURCE_NASA_APOD_EN

    def extract(self, year, month, day, update_existing=False, max_thumb_size=None, use_cached=False):
        if max_thumb_size:
            logger.debug('extractor nasa_apod_en: max_thumb_size not available')
        potd_at = date(year=year, month=month, day=day)
        potd_kwargs = {'potd_at': potd_at, 'source_type': self.source_type}
        try:
            potd = POTD.objects.get(**potd_kwargs)
            if not update_existing:
                logger.info('extractor nasa_apod_en: potd already existing and not updating: {}'.format(potd))
                return
            else:
                logger.debug('extractor nasa_apod_en: using already existing potd: {}'.format(potd_kwargs))
        except POTD.DoesNotExist:
            logger.debug('extractor nasa_apod_en: creating new potd for {}'.format(potd_kwargs))
            potd = POTD(**potd_kwargs)

        source_potd_url = NASAAPODEnExtractor.APOD_DETAIL_URL_BY_DATE.format(
            yy=str(year)[-2:], mm=int(month), dd=int(day))
        potd.source_url = source_potd_url
        logger.debug('extractor nasa_apod_en: source potd url: {}'.format(source_potd_url))
        if use_cached and potd.raw_scaping_data_binary_compressed:
            response = self._FakeResponse(potd.raw_scaping_data_binary_uncompressed)
            logger.debug('extractor nasa_apod_en: using cached markup')
        else:
            response = requests.get(source_potd_url)
            potd.raw_scaping_data_binary_compressed = self._compress(response.content)

        if response.ok:
            # Marked up like it's 1995...
            tree = html.fromstring(response.content)
            _explanation = tree.xpath("//b[starts-with(normalize-space(text()),'Explanation')]/parent::p")[0]
            h = HTML2Text()
            h.ignore_links = True
            potd.description = h.handle(tostring(_explanation, encoding='unicode')).strip().replace(
                '** Explanation: ** ', '').strip()
            potd.title = tree.xpath("//img[starts-with(@src,'image/')][1]/following::b[1]")[0].text_content().strip()
            _image_filename = tree.xpath("//img[starts-with(@src,'image/')][1]/attribute::src")[0]
            if not _image_filename.lower().endswith(settings.ALLOWED_IMAGE_EXTENSIONS):
                logger.info('extractor nasa_apod_en: not a matching potd type: {}'.format(_image_filename))
                return
            potd.image_url = NASAAPODEnExtractor.APOD_BASE_URL + _image_filename
            # nice to have's
            try:
                center_elem = tree.xpath("//img[starts-with(@src,'image/')][1]/following::b[1]/..")[0]
                center_elem_html = tostring(center_elem, encoding='unicode').replace('\n', ' ')
                # Ugly, but works...
                # TODO: reimplement this with elem.drop_tree()
                _copyright = NASAAPODEnExtractor.UGLY_TAG_STRIP_RE.sub(' ', center_elem_html)
                h.ignore_links = False
                potd.copyright_info = h.handle(_copyright.strip()).replace('\n', ' ')
                _image_hires_url = tree.xpath("//img[contains(@src,'image/')][1]/../attribute::href")[0]
                if _image_hires_url.lower().endswith(settings.ALLOWED_IMAGE_EXTENSIONS):
                    potd.image_thumbnail_url = potd.image_url
                    if _image_hires_url.startswith('http'):
                        potd.image_url = _image_hires_url
                    else:
                        potd.image_url = NASAAPODEnExtractor.APOD_BASE_URL + _image_hires_url
            except Exception as e:
                logger.debug('extractor nasa_apod_en: fail for additional info: {}'.format(e))
        else:
            logger.error('extractor nasa_apod_en: http status code {} for url: {}'.format(
                response.status_code, source_potd_url))
            response.raise_for_status()

        potd.retrieved_from_source_at = now()

        potd.save()

        logger.info('extractor nasa_apod_en: potd okay for {}-{}-{} "{}"'.format(
            year, month, day, potd.title))

        return potd
