import json
from django.conf import settings
from picture_of_the_day.models import POTD


def core(request):
    context = {
        'DEBUG': settings.DEBUG,
        'ACTIVE_SETTING': settings.ACTIVE_SETTING,
        'NAME_OF_SITE_LONG': settings.NAME_OF_SITE_LONG,
        'NAME_OF_SITE_SHORT': settings.NAME_OF_SITE_SHORT,
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'TRANS': json.dumps({s: str(t) for s, t in POTD.PICTURE_SOURCE_CHOICES}),
    }
    return context
