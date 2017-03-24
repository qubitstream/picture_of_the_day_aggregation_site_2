import os
from fractions import Fraction
from unidecode import unidecode
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils.text import slugify
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


class POTD(models.Model):
    PICTURE_SOURCE_UNSPECIFIED = 'unspecified'
    PICTURE_SOURCE_WIKIPEDIA_EN = 'wikipedia_en'
    PICTURE_SOURCE_CHOICES = (
        (PICTURE_SOURCE_UNSPECIFIED, _('Unspecified source')),
        (PICTURE_SOURCE_WIKIPEDIA_EN, _('Wikipedia (English)')),
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
        allow_unicode=True,
        unique_for_date='potd_at',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('last update'),
    )

    retrieved_from_source_url_at = models.DateTimeField(
        verbose_name=_('datetime retrieved from source URL'),
    )

    potd_at = models.DateField(
        verbose_name=_('date on which this picture was "picture of the day"'),
    )

    description = models.TextField(
        verbose_name=_('description of the picture'),
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
        blank=False,
        width_field='width',
        height_field='height',
        verbose_name=_('picture of the day image file')
    )

    raw_scraping_data_image = models.TextField(
        blank=True,
        verbose_name=_('raw scraping data for image'),
        editable=False
    )

    @property
    def aspect_ratio(self):
        return '{0.numerator}:{0.denominator}'.format(Fraction(self.width, self.height)) if self.height else _('N/A')

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

    def __str__(self):
        return '{0} | {1.year:0>4}-{1.month:0>2}-{1.day:0>2}: {2.title}'.format(
            self.get_source_type_display(), self.potd_at, self)

    def __repr__(self):
        return 'pk={0.pk} potd_at={0.potd_at} source_type={0.source_type} title={0.title} | url={1}'.format(self,
            self.get_absolute_url())

    class Meta:
        ordering = ['-potd_at']
        verbose_name = _('picture of the day')
        verbose_name_plural = _('pictures of the day')
        unique_together = ('potd_at', 'source_type')
