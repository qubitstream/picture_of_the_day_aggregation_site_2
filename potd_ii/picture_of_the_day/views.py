from datetime import date, datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, Http404
from django.views.decorators.cache import cache_page
from django.views import generic
from django.conf import settings
from django.template import defaultfilters
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
import django_filters
from .models import POTD
from .serializers import POTDSerializer

import logging

logger = logging.getLogger(__name__)


class POTDListView(generic.ListView):
    paginate_by = 6
    context_object_name = 'potds'
    template_name = 'potd_list.html'
    queryset = POTD.objects.published()

    def get_context_data(self, **kwargs):
        context = super(POTDListView, self).get_context_data(**kwargs)
        ps = POTDSerializer(self.get_queryset(), many=True)
        context['initial_data_json'] = JSONRenderer().render(ps.data)
        return context


@cache_page(settings.CACHE_TIME_POTD_DETAIL)
def potd_detail(request, year, month, day, source_type=POTD.PICTURE_SOURCE_WIKIPEDIA_EN, slug=''):
    potd_date = date(year=int(year), month=int(month), day=int(day))
    potd = get_object_or_404(POTD.objects.published(), potd_at=potd_date, source_type=source_type)

    if slug != potd.slug or len(year) != 4 or len(month) != 2 or len(day) != 2:
        return HttpResponsePermanentRedirect(potd.get_absolute_url())

    return render(request, template_name='picture_of_the_day/potd_detail.html', context={
        'potd': potd,
        'initial_data_json': JSONRenderer().render(POTDSerializer(potd).data),
        'month_human_readable': defaultfilters.date(potd_date, 'F'),
    })


class POTDFilter(django_filters.rest_framework.FilterSet):
    min_date = django_filters.DateFilter(name='potd_at', lookup_expr='gte')
    max_date = django_filters.DateFilter(name='potd_at', lookup_expr='lte')
    before_date = django_filters.DateFilter(name='potd_at', lookup_expr='lt')
    after_date = django_filters.DateFilter(name='potd_at', lookup_expr='gt')

    class Meta:
        model = POTD
        fields = ['source_type', 'min_date', 'max_date', 'before_date', 'after_date']


class POTDViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = POTDSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = POTDFilter
    queryset = POTD.objects.published()
