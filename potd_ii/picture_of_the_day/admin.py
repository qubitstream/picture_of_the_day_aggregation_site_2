from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from .models import POTD


class PTDAdmin(admin.ModelAdmin):
    def image_format(self, obj):
        if obj.image:
            return '{0.width}x{0.height}px (aspect {0.aspect_ratio}), size {1}'.format(
                obj, filesizeformat(obj.image.size))
        else:
            return 'N/A'

    image_format.short_description = _('image details')
    list_display = 'source_type,potd_at,is_published,title,image_format'.split(',')
    readonly_fields = ('slug', 'width', 'height')
    fieldsets = (
        (None, {
            'fields': ('source_type', 'potd_at', 'is_published', 'title', 'slug', 'description',
                       'copyright_info', 'image', 'source_url', 'detail_url',
                       'image_url', 'image_thumbnail_url', 'retrieved_from_source_at'),
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('width', 'height', 'raw_scraping_data_binary_string')
        }),
    )
    readonly_fields = ('source_url', 'detail_url', 'width', 'height',
                       'retrieved_from_source_at', 'image_url', 'image_thumbnail_url',
                       'updated_at', 'slug', 'potd_at', 'raw_scraping_data_binary_string')


admin.site.register(POTD, PTDAdmin)
