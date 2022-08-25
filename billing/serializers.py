from rest_framework import serializers

from users.serializers import UserSerializer
from billing.models import BillingProfile


class BillingProfileSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  # country = serializers.SerializerMethodField()

  class Meta:
    model = BillingProfile
    fields = ['id', 'user', 'first_name', 'last_name', 'phone', 'email', 'address', 'city']
