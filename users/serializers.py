from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import ProfileUser


User = get_user_model()

class ProfileUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProfileUser
    fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
  profile_user = ProfileUserSerializer()

  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'profile_user', 'roll']

  def create(self, validated_data):
    profile_data = validated_data.pop('profile_user')
    profile = ProfileUser.objects.create(**profile_data)
    user = User.objects.create(profile_user=profile, **validated_data)
    return user


class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(required=True)
  password = serializers.CharField(required=True)


class UserSerializerWithToken(UserSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'phone']

  def get_token(self, obj):
    token = RefreshToken.for_user(obj)
    return token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
    data = super().validate(attrs)

    serializer = UserSerializerWithToken(self.user).data
    for key, value in serializer.items():
      data[key] = value

    return data

