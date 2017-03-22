from django.conf import settings


def core(request):
    context = {
        'DEBUG': settings.DEBUG,
        'ACTIVE_SETTING': settings.ACTIVE_SETTING,
        'NAME_OF_SITE_LONG': settings.NAME_OF_SITE_LONG,
        'NAME_OF_SITE_SHORT': settings.NAME_OF_SITE_SHORT,
        'SITE_DOMAIN': settings.SITE_DOMAIN,
    }
    return context
