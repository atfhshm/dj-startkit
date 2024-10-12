"""
This module contains shared serializers that are commonly used within the project
"""

from rest_framework import serializers


class DeleteMethodResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(
        required=True,
        help_text="Indicates whether the object was successfully deleted or not.",
    )


class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()
