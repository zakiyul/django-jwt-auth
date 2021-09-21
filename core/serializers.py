from re import search
from django.db import models
from rest_framework import fields, serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username']

class UserSerializerWithToken(serializers.ModelSerializer):
  token = serializers.SerializerMethodField()
  password = serializers.CharField(write_only=True)

  def get_token(self, obj):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encoded_handler = api_settings.JWT_ENCODED_HANDLER

    payload = jwt_payload_handler(obj)
    token = jwt_encoded_handler(payload)

    return token

  def create(self, validate_data):
    password = validate_data.pop('password', None)
    instance = self.Meta.module(**validate_data)
    if password is not None:
      instance.set_password(password)
    instance.save()
    return instance
  
  class Meta:
    model = User
    fields = ['token','username','password']