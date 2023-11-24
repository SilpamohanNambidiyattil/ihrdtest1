from __future__ import annotations

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.response import Response

from users.serializers import LoginSerializer
from users.serializers import RegisterSerializer
from users.serializers import UserSerializer
from core_viewsets.custom_viewsets import CreateViewSet
from core_viewsets.custom_viewsets import ListViewSet

from django.contrib.auth import authenticate,login

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from rest_framework import authentication
from rest_framework import permissions



# Create your views here.


class RegisterViewSet(CreateViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):

        email = request.data.get('email')
        password = request.data.get('password', None)
        phone_number = request.data.get('phone_number')

        # TODO: Validations


        user = get_user_model().objects.create_user(request.data)

        return Response(
            {'code': 200, 'message': 'success', 'user_id': user._get_pk_val()},
        )


class LoginViewSet(CreateViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        # TODO: validation
        user = authenticate(request,email=email, password=password)
        if user:
            login(request,user)
            refresh=RefreshToken.for_user(user)
            data = {
                'token': str(refresh.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        
        # return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)


        user_obj = get_user_model().objects.get(email=email, password=password)
        user_obj.last_login = timezone.now()
            # TODO:  generate token with jwt library
            # TODO: Update the Login activity

        user_obj.last_login = timezone.now()
        return Response(
                {
                    'code': 200,
                    'message': 'success',
                    'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwNzk4MTA4LCJpYXQiOjE3MDA3OTc4MDgsImp0aSI6ImUxYjZhMjA2ZjBkNDQ3NDg5YTgyZDExYWFmMTFiNjY0IiwidXNlcl9pZCI6MX0.0r_VQsKOPwUCAHpN-WljQ7SUK7hSeTfsrjCQoYQc5Hs',
                    'refresh_token': 'refresh_token',
                    'user_id': user_obj.pk,
                    'name': user_obj.first_name,
                    'email': user_obj.email,
                    'last_login': user_obj.last_login,
                },
            )
    
    
   

class MeViewSet(ListViewSet):
    authentication_classes = ()  # ToDO Specify Auth class
    permission_classes = ()
    serializer_class = UserSerializer  # ToDO Specify serializer_class class
    queryset = get_user_model().objects.all()

    def list(self, request, *args, **kwargs):
        # ToDO:  Add your code
        id=kwargs.get("pk")
        obj=get_user_model().objects.get(id=id)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
