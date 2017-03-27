import os
import logging
import requests
from datetime import date, timedelta
from django.core.files.base import ContentFile
from django.utils.timezone import now
from django.conf import settings
from easy_thumbnails.templatetags import thumbnail
from easy_thumbnails.files import get_thumbnailer
from ..models import POTD
logger = logging.getLogger('management')


class BaseExtractor:
    def __init__(self):
        self.source_type = POTD.PICTURE_SOURCE_UNSPECIFIED  # overwrite in subclasses
        self.max_thumb_size = settings.THUMBNAIL_MAX_SCRAPE_SIZE  # will be default value for extract

    def extract(self, year, month, day, update_existing=False, max_thumb_size=None):
        """Returns a new (or updated) POTD instance (without downloading the image)"""
        raise NotImplementedError('Not implemented in extractor base class')


def download_image(potd, redownload=False):
    """Downloads the image to the corresponding potd, returns True if image (re-)downloaded"""
    if potd.image and not redownload:
        logger.info('skipping re-downloading of image for {}'.format(potd))
        return False
    if not potd.image_url:
        logger.warning('no image URL for {}'.format(potd))
        return False
    if not potd.pk:
        potd.save()
    try:
        # TODO: figure out why thumbnails don't get deleted this way
        thumbnailer = get_thumbnailer(potd.image)
        thumbnails_deleted = thumbnailer.delete_thumbnails()
        logger.debug('extractor image download: deleted {} thumbnails'.format(thumbnails_deleted))

        # prefer the smaller thumbnail url if available
        image_url = potd.image_thumbnail_url or potd.image_url
        image_response = requests.get(image_url)
        potd.image.delete(False)
        potd.image.save(os.path.split(potd.image_url)[1], ContentFile(image_response.content))
        # pre-create thumbnails by getting the url
        for thumb_type in settings.THUMBNAIL_ALIASES_TO_PREGENERATE:
            logger.debug('extractor image download: thumb [{}]: {}'.format(
                thumb_type, thumbnail.thumbnail_url(potd.image, thumb_type)))
        return True
    except Exception as e:
        logger.error('extractor image download failure: {}'.format(e))
        return False


def extract_range(start_year=None, start_month=None, start_day=None,
                  end_year=None, end_month=None, end_day=None,
                  source_types=None, update_existing=False, redownload_image=False):
    """Extracts info & downloads the image for a given date range and source type.
    If no end numbers are given, the start date's numbers are filled in.
    
    Returns tuple: days_processed, potds_extracted, images_downloaded
    """
    start_date = date(
        year=start_year or now().year,
        month=start_month or now().month,
        day=start_day or now().day)
    end_date = date(
        year=end_year or start_date.year,
        month=end_month or start_date.month,
        day=end_day or start_date.day)
    if end_date < start_date:
        start_date, end_date = end_date, start_date
    if start_date < settings.POTD_AT_START:
        logger.info('start date is too early')
        start_date = settings.POTD_AT_START
    single_day = timedelta(days=1)

    if source_types is None:
        source_types = [
            source_type for source_type, _ in POTD.PICTURE_SOURCE_CHOICES
            if source_type != POTD.PICTURE_SOURCE_UNSPECIFIED
        ]

    from . import wikipedia_en
    extractors = {
        POTD.PICTURE_SOURCE_WIKIPEDIA_EN: wikipedia_en.WikipediaEnExtractor(),
    }

    days_processed, potds_extracted, images_downloaded = 0, 0, 0

    d = start_date
    while d <= end_date:
        if d >= settings.POTD_AT_START:
            days_processed += 1
            for source_type in source_types:
                if source_type in extractors:
                    try:
                        potd = extractors[source_type].extract(d.year, d.month, d.day, update_existing=update_existing)
                        if potd:
                            potds_extracted += 1
                            has_downloaded = download_image(potd, redownload=redownload_image)
                            images_downloaded += 1 if has_downloaded else 0
                    except Exception as e:
                        logger.debug('extract range: {}'.format(e))
                else:
                    logger.warning('extract range: no extractor for source type {}'.format(source_type))
        d += single_day

    logger.info('extract range: processed {} days, {} potds extracted, {} images downloaded'.format(
        days_processed, potds_extracted, images_downloaded
    ))
    return days_processed, potds_extracted, images_downloaded
