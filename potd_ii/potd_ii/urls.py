from django.conf.urls import url
from django.views import  generic
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^$', generic.TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^admin/', admin.site.urls),
]

if 'local' in settings.ACTIVE_SETTING:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
