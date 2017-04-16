import os
import lzma
from fractions import Fraction
from unidecode import unidecode
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.conf import settings
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
import logging

logger = logging.getLogger(__name__)


def image_upload_path(instance, filename):
    _, ext = os.path.splitext(filename.lower())
    basename = slugify(unidecode(instance.title)[:40], allow_unicode=False)
    upload_to = ('potds/{0.year:0>4}/{0.month:0>2}/{0.day:0>2}/'
                 '{1}__{0.year:0>4}-{0.month:0>2}-{0.day:0>2}__{2}{3}').format(
        instance.potd_at, instance.source_type, basename, ext
    )
    return upload_to


class POTDQuerySet(models.QuerySet):
    def potd_at_year(self, year):
        return self.filter(potd_at__year=year)

    def potd_at_month(self, month):
        return self.filter(potd_at__month=month)

    def potd_at_day(self, day):
        return self.filter(potd_at__day=day)

    def published(self):
        return self.filter(is_published=True)

    def earlier_than(self, cmp_date, max_items=1):
        return self.order_by('-potd_at').filter(potd_at__lt=cmp_date)[:max_items]

    def later_than(self, cmp_date, max_items=1):
        return self.order_by('potd_at').filter(potd_at__gt=cmp_date)[:max_items]

    def earlier_than_that(self, that_potd, max_items=1):
        return self.earlier_than(that_potd.potd_at, max_items=max_items)

    def later_than_that(self, that_potd, max_items=1):
        return self.later_than(that_potd.potd_at, max_items=max_items)


class POTD(models.Model):
    PICTURE_SOURCE_UNSPECIFIED = 'unspecified'
    PICTURE_SOURCE_WIKIPEDIA_EN = 'wikipedia_en'
    PICTURE_SOURCE_NASA_APOD_EN = 'nasa_apod_en'
    PICTURE_SOURCE_CHOICES = (
        (PICTURE_SOURCE_UNSPECIFIED, _('Unspecified source')),
        (PICTURE_SOURCE_WIKIPEDIA_EN, _('Wikipedia (English)')),
        (PICTURE_SOURCE_NASA_APOD_EN, _('NASA Astronomy Picture of the Day (English)')),
    )

    title = models.CharField(
        blank=False,
        max_length=400,
        verbose_name=_('title of the picture')
    )

    source_type = models.CharField(
        max_length=36,
        choices=PICTURE_SOURCE_CHOICES,
        default=PICTURE_SOURCE_UNSPECIFIED,
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name=_('is published')
    )

    slug = models.SlugField(
        max_length=100,
        allow_unicode=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('last update'),
    )

    retrieved_from_source_at = models.DateTimeField(
        verbose_name=_('datetime retrieved from source'),
        auto_now_add=True,
    )

    potd_at = models.DateField(
        verbose_name=_('date featured as picture of the day'),
        db_index=True
    )

    source_url = models.URLField(
        verbose_name=_('source url'),
        help_text=_('URL for the image page, e.g. the wikimedia commons page'),
        editable=False,
        blank=True
    )

    detail_url = models.URLField(
        verbose_name=_('detail url'),
        help_text=_('URL for additional information, e.g. a wikipedia article corresponding to the image'),
        editable=False,
        blank=True,
    )

    image_url = models.URLField(
        verbose_name=_('image url'),
        help_text=_('URL for the direct link to the image, for the highest res available'),
        editable=False,
        blank=True,
    )

    image_thumbnail_url = models.URLField(
        verbose_name=_('thumbnail image url'),
        help_text=_('URL for the direct link to a smaller image, preferable and sufficient for importing'),
        editable=False,
        blank=True,
    )

    description = models.TextField(
        verbose_name=_('description of the picture'),
        help_text=_('Markdown is allowed'),
    )

    copyright_info = models.TextField(
        verbose_name=_('copyright information'),
        help_text=_('Markdown is allowed'),
        blank=True,
    )

    width = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_('width of image')
    )

    height = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name=_('height of image')
    )

    image = models.ImageField(
        upload_to=image_upload_path,
        blank=True,
        width_field='width',
        height_field='height',
        verbose_name=_('picture of the day image file')
    )

    # this field for avoiding parsing the source sites again and again. especially during testing
    # yes, storing binary in the db is bad - this data can be stored in files if the need arises
    raw_scaping_data_binary_compressed = models.BinaryField(
        blank=True,
        verbose_name=_('lzma compressed raw scraping data for image'),
        editable=False
    )

    @property
    def aspect_ratio(self):
        return '{0.numerator}/{0.denominator}'.format(Fraction(self.width, self.height)) if self.image else _('N/A')

    @property
    def raw_scaping_data_binary_uncompressed(self):
        retval = b''
        if self.raw_scaping_data_binary_compressed:
            try:
                retval = lzma.decompress(self.raw_scaping_data_binary_compressed)
            except Exception as e:
                logger.debug('error decompressing raw_scraping_data_binary for {}: {}'.format(self, e))
        return retval

    @property
    def raw_scraping_data_binary_string(self):
        try:
            return self.raw_scaping_data_binary_uncompressed.decode('utf8')
        except:
            pass
        return ' - ' + _('Error decompressing') + ' _ '

    def thumbnail_full_url(self, thumb_preset='potd400x400'):
        return settings.SITE_DOMAIN + thumbnail_url(self.image, thumb_preset)

    def thumbnail_full_urls(self):
        """a dict of all thumbnails"""
        return {key: self.thumbnail_full_url(key) for key in settings.THUMBNAIL_ALIASES[''].keys()}

    objects = POTDQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)[:100]
        super(POTD, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'potd.picture_of_the_day.detail',
            kwargs={
                'year': '{:0>4}'.format(self.potd_at.year),
                'month': '{:0>2}'.format(self.potd_at.month),
                'day': '{:0>2}'.format(self.potd_at.day),
                'source_type': self.source_type,
                'slug': self.slug,
            })

    def get_full_url(self):
        return settings.SITE_DOMAIN + self.get_absolute_url()

    def __str__(self):
        return '{0} | {1.year:0>4}-{1.month:0>2}-{1.day:0>2}: {2.title}'.format(
            self.get_source_type_display(), self.potd_at, self)

    def __repr__(self):
        return 'pk={0.pk} potd_at={0.potd_at} source_type={0.source_type} title={0.title} | url={1}'.format(self,
                                                                                                            self.get_absolute_url())

    class Meta:
        ordering = ['-potd_at', 'source_type']
        get_latest_by = 'potd_at'
        verbose_name = _('picture of the day')
        verbose_name_plural = _('pictures of the day')
        unique_together = ('potd_at', 'source_type')
