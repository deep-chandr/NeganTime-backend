

from authentication.constants import MIN_PASSWORD_LENGTH
from negantime.drf_utils import ApiRenderer, Response
from rest_framework import mixins, status
from rest_framework.decorators import (api_view, permission_classes,
                                       renderer_classes)
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Profile, User
from negantime.settings import AWS_S3_ACCESS_KEY_ID, AWS_S3_BUCKET, AWS_S3_REGION, AWS_S3_SECRET_ACCESS_KEY

from .renderers import UserJSONRenderer
from .serializers import (LoginSerializer, ProfileSerializer, RegistrationSerializer,
                          UserSerializer,
                          UserSerializer2)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    renderer_classes = (ApiRenderer,)
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        username = user.get('username')
        email = user.get('email')
        password = user.get('password')

        if User.all_objects.filter(username=username).count():
            raise APIException("Username unavailable")

        if User.all_objects.filter(email=email).count():
            raise APIException("Account already exists")

        if len(password) < MIN_PASSWORD_LENGTH:
            raise APIException("Account already exists")

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (ApiRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (ApiRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        username = request.query_params.get('username')

        if username:
            try:
                user = User.objects.get(username=username)
                return Response(UserSerializer2(user).data)
            except User.DoesNotExist:
                raise APIException('Invalid user')

        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if not request.user:
            raise PermissionDenied()

        serializer_data = request.data.get('user', {})
        profile_data = serializer_data.pop(
            'profile') if 'profile' in serializer_data else {}

        if serializer_data['id'] != request.user.id:
            raise PermissionDenied()

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        #  saving profile data
        profile_serialized = ProfileSerializer(Profile.objects.get(
            user=request.user), data=profile_data, partial=True)
        profile_serialized.is_valid(raise_exception=True)
        profile_serialized.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@renderer_classes([ApiRenderer, ])
@permission_classes((IsAuthenticated,))
def verify_token(request):
    try:
        res_data = UserSerializer(request.user).data
        return Response(res_data, msg='Token verified successfully')
    except Exception as err:
        raise APIException("Invalid token")


@api_view(["GET"])
@renderer_classes([ApiRenderer, ])
@permission_classes((IsAuthenticated,))
def get_credential(request):
    res_data = {
        'AWS_S3_ACCESS_KEY_ID': AWS_S3_ACCESS_KEY_ID,
        'AWS_S3_SECRET_ACCESS_KEY': AWS_S3_SECRET_ACCESS_KEY,
        'AWS_S3_REGION': AWS_S3_REGION,
        'AWS_S3_BUCKET': AWS_S3_BUCKET
    }
    return Response(res_data, msg='Success')


class ProfileFollow(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (ApiRenderer,)
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise APIException('Profile not found')

    def get(self, request):
        profile = self.get_object()
        data = list(profile.user_followers.all().values_list('id', flat=True))
        return Response(data)

    def update(self, request):
        profile = self.get_object()
        user_followers = request.data.pop('user_followers', [])
        action = request.data.pop('action', None)
        if action == 'add':
            profile.user_followers.add(*user_followers)
        elif action == 'remove':
            profile.user_followers.remove(*user_followers)
        else:
            raise APIException('Invalid action')

        # data = UserSerializer(profile.user_followers.all(), many=True).data
        data = list(profile.user_followers.all().values_list('id', flat=True))
        return Response(data)
