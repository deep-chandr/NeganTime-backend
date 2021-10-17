import copy
import datetime
import json
from operator import attrgetter

from authentication.models import User
from authentication.serializers import UserSerializer
from django.db.models import ExpressionWrapper, F, FloatField, Q, Sum
from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers

from blog.models import Blog


class BlogSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['author'] = UserSerializer(
            instance.author, exclude=('token', )).data
        return data
