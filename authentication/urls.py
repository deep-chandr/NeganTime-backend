from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, verify_token

app_name = 'authentication'
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),     # open api
    path('users/', RegistrationAPIView.as_view()),
    path('users/verify/', verify_token),                    # authenticated
    path('users/login/', LoginAPIView.as_view()),
]
