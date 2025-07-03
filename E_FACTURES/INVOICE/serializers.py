from rest_framework import serializers
from .models import facture

class FactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = facture
        fields = '__all__'
