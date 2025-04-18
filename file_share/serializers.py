from rest_framework import serializers
from file_share.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'user', 'file', 'file_name', 'comment', 'uploaded_at', 'downloaded_at', 'size', 'special_link']
        read_only_fields = ['id', 'uploaded_at', 'downloaded_at', 'size', 'special_link']

    def create(self, validated_data):
        if 'file_name' in validated_data:
            validated_data.pop('file_name')
        return super().create(validated_data)