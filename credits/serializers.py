from rest_framework import serializers
from .models import CreditConfiguration


class CreditConfigurationSerializer(serializers.ModelSerializer):
    installment_options_list = serializers.SerializerMethodField()

    class Meta:
        model = CreditConfiguration
        fields = ('id', 'interest_rate', 'min_installments', 'max_installments',
                  'installment_options', 'installment_options_list', 'updated_at')

    def get_installment_options_list(self, obj):
        return obj.get_installment_options_list()
