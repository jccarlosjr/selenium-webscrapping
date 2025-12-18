from rest_framework import serializers


class ScrapperSerializer(serializers.Serializer):
    cpf = serializers.CharField()

