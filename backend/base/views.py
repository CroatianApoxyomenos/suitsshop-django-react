from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from django.contrib.auth.hashers import make_password
from rest_framework import status
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def hello(request):
    return render(request, 'hello.html', {'name': 'George'})


class UserRegisterViewSet(APIView):
    def post(self, request):
        data = request.data
        try:
            user = User.objects.create(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=make_password(data['password'])
            )
            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'A user with that username or email already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
