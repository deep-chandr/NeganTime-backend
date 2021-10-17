
from rest_framework import serializers
from django_restql.mixins import DynamicFieldsMixin

from blog.models import Blog
from authentication.serializers import UserSerializer


class BlogSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['author'] = UserSerializer(
            instance.author, exclude=('token', )).data
        return data
