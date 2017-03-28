from rest_framework import serializers
from .models import POTD


class POTDSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField('full_url_field')
    neighbours = serializers.SerializerMethodField('neighbours_field')

    def full_url_field(self, obj):
        return obj.get_full_url()

    def neighbours_field(self, obj):
        published = POTD.objects.published()
        previous_potds = published.earlier_than_that(obj)
        next_potds = published.later_than_that(obj)
        return {
            'previous_id': previous_potds[0].pk if previous_potds else None,
            'next_id': next_potds[0].pk if next_potds else None,
        }

    class Meta:
        model = POTD
        fields = ('id,source_type,potd_at,source_url,detail_url,title,description,full_url,'
            'image,width,height,aspect_ratio,thumbnail_full_urls,neighbours').split(',')

