from rest_framework import serializers

from .models import ImageModel


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = (
            'initial_image',
            'result_json',
            'result_image',
        )

    def get_initial_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.initial_image.url)

    def get_result_image_url(self, obj):
        request = self.context.get("request")
        if obj.result_image.url:
            return request.build_absolute_uri(obj.result_image.url)
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['initial_image'] = self.get_initial_image_url(instance)
        # representation['result_image'] = self.get_result_image_url(instance)
        return representation
