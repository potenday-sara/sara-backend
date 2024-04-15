from rest_framework.serializers import Serializer


class RequestSerializer(Serializer):
    def create(self, validated_data):  # pragma: no cover
        pass

    def update(self, instance, validated_data):  # pragma: no cover
        pass
