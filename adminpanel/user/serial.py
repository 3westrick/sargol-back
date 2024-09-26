from rest_framework import serializers
from base.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

class UserSerial(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email'
            ]
        
class UserPermission(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = [
            'user_permissions'
        ]
    
class UserTestSerial(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], allow_blank=True)
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'name',
            'username',
            'phone',
            'country',
            'city',
            'address',
            'post_code',
            'password',
            'email',
            'user_permissions',
            'groups',
            'is_staff'
            ]
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if len(validated_data['password']) == 0:
            validated_data['password'] = instance.password
        else:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)
    
    def get_name(self, user: User):
        return user.get_full_name()