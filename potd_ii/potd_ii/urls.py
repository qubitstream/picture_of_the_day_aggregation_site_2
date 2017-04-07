from django.conf.urls import url, include
from django.views import generic
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
import picture_of_the_day.views


router = routers.DefaultRouter()
router.register(r'potds', picture_of_the_day.views.POTDViewSet, 'potd-view')

urlpatterns = [
    url(r'^$', picture_of_the_day.views.POTDListView.as_view(), name='potd.picture_of_the_day.list'),
    url(r'^(?P<year>\d{4,})/(?P<month>\d+)/(?P<day>\d+)/(?P<source_type>[a-zA-Z_\-]+)/(?P<slug>.*)/$',
        picture_of_the_day.views.potd_detail, name='potd.picture_of_the_day.detail'),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
]

if 'local' in settings.ACTIVE_SETTING:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    from django.templatetags.static import static as static_templatetag
    favicon_view = generic.RedirectView.as_view(url=static_templatetag('favicon.ico'), permanent=True)
    urlpatterns += [url(r'^favicon\.ico$', favicon_view)]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
