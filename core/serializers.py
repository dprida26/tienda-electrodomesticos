from rest_framework import serializers
from .models import CompanyConfiguration


class CompanyConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyConfiguration
        fields = (
            'id', 'company_name', 'phone', 'whatsapp_number', 'email', 'address',
            'city', 'country', 'facebook_url', 'instagram_url', 'twitter_url',
            'youtube_url', 'business_hours', 'shipping_time', 'updated_at'
        )
        read_only_fields = ('id', 'updated_at')
