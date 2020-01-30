from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from . import serializers
from django.contrib.auth import authenticate, login, logout, get_user_model


User = get_user_model()


class RegisterView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        """Регистрация нового пользователя"""
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "ok"
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.CreateAPIView):
    """Логин"""
    permission_classes = ()
    authentication_classes = ()
    serializer_class = serializers.LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cd = serializer.validated_data
        user = authenticate(request,
                            username=cd['email'],
                            password=cd['password'])
        if user is not None:
            login(request, user)
            return Response(
                {
                    'message': 'ok'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'message': 'wrong_username_or_password'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    """Выйти из системы"""

    def post(self, request):
        logout(request)
        return Response(
            {
                'message': 'ok'
            },
            status=status.HTTP_200_OK
        )
