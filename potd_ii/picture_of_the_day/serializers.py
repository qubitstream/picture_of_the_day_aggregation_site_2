from rest_framework import serializers
from .models import POTD


class POTDSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField('full_url_field')

    def full_url_field(self, obj):
        return obj.get_full_url()

    class Meta:
        model = POTD
        fields = ('id,source_type,potd_at,source_url,detail_url,title,description,full_url,'
            'image,width,height,aspect_ratio,thumbnail_full_urls,copyright_info').split(',')

