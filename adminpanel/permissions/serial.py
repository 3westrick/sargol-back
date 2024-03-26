from rest_framework import serializers
from django.contrib.auth.models import Permission

class PermissionSerial(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'codename'
            ]
        
