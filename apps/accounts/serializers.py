from rest_framework import serializers
from .models import Account, Consumer, Client


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["name", "address", "ssn"]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["name"]


class AccountSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    consumers = ConsumerSerializer(many=True, read_only=True)

    class Meta:
        model = Account
        fields = ["client_reference_no", "client", "consumers", "balance", "status"]
