"""negantime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('blog/', BlogList.as_view(), name='blog_list'),

    path('blog/trending/', TrendingList.as_view(), name='blog_trending_list'),
    path('blog/popular/', PopularList.as_view(), name='blog_popular_list'),
    path('blog/<int:pk>', BlogDetail.as_view(), name='blog_detail'),

    path('', index, name='blog')
]
