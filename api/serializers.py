from rest_framework import serializers

from .models import Lender

class LenderSerializer(serializers.ModelSerializer):
    """
    To be used for POST / PUT requests
    """
    class Meta:
        model = Lender
        fields = '__all__'

class LenderReadOnlySerializer(serializers.ModelSerializer):
    """
    To be used for GET requests such as list and retrieve to avoid lazy DRF calls
    read_only_fields are required to speed up the API response for large data volumes
    """
    class Meta:
        model = Lender
        fields = ['id', 'name', 'code', 'upfront_commission_rate', 'trial_commission_rate', 'active']
        read_only_fields = fields

class LenderCSVSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lender
        fields = ['name', 'code', 'upfront_commission_rate', 'trial_commission_rate', 'active']
    
    def to_internal_value(self, obj):
        """
        "Translate" human readable fields back into django fields
        """
        obj = {
            "name": obj.pop("Name", ""),
            "code": obj.pop("Code", ""),
            "upfront_commission_rate": obj.pop("Upfront Commission Rate"),
            "trial_commission_rate": obj.pop("Trial Commission Rate"),
            "active": obj.pop("Active")
        }
        return super(LenderCSVSerializer, self).to_internal_value(obj)