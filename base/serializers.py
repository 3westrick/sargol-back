from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from base.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = (user.is_staff or user.is_superuser)
        # elif 
        return token

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    name = serializers.SerializerMethodField(read_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Password fields didn't match."})
        return super().validate(attrs)

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user
    
    def get_name(self, user: User):
        return user.get_full_name()


    class Meta:
        model = User
        fields = ( "id",'name','phone','first_name','last_name','address' ,"username", "email", "password", "password_confirm")


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