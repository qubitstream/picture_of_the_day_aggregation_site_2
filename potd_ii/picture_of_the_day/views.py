from datetime import date, datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, Http404
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.template import defaultfilters
from .models import POTD
import logging
logger = logging.getLogger(__name__)


@cache_page(settings.CACHE_TIME_POTD_DETAIL)
def potd_detail(request, year, month, day, source_type=POTD.PICTURE_SOURCE_WIKIPEDIA_EN, slug=''):
    potd_date = date(year=int(year), month=int(month), day=int(day))
    potd = get_object_or_404(POTD.objects.published(), potd_at=potd_date, source_type=source_type)

    if slug != potd.slug or len(year) != 4 or len(month) != 2 or len(day) != 2:
        return HttpResponsePermanentRedirect(potd.get_absolute_url())

    return render(request, template_name='picture_of_the_day/potd_detail.html', context={
        'potd': potd,
        'month_human_readable': defaultfilters.date(potd_date, 'F'),
    })
