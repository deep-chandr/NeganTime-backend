from django.db.models import F
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from django.http import HttpResponse
# from order_management_backend.renderers import ApiRenderer

from .serializers import BlogSerializer
from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class BlogList(generics.ListCreateAPIView):
    # renderer_classes = [ApiRenderer]
    queryset = Blog.objects.all().order_by('-id')
    serializer_class = BlogSerializer


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    # renderer_classes = [ApiRenderer]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    

