from rest_framework import generics
from rest_framework.response import Response
from django.http import HttpResponse
from negantime.drf_utils import ApiRenderer

from .serializers import BlogSerializer
from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class BlogList(generics.ListCreateAPIView):
    renderer_classes = [ApiRenderer]
    queryset = Blog.objects.all().order_by('-id')
    serializer_class = BlogSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        qs = super().get_queryset()
        qs = qs.filter(author__username=username)
        return qs

    def post(self, request):
        data = request.data
        data['author'] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = [ApiRenderer]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
