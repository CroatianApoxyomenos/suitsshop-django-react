from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .models import Product, CustomUser
from .serializers import ProductSerializer
from jsonschema import validate
import jsonschema
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
        schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "minLength": 4,
                    "pattern": "^[A-Za-z0-9]+$"
                },
                "password": {
                    "type": "string",
                    "minLength": 8,
                    "pattern": "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$"
                },
                "email": {
                    "type": "string",
                    "pattern": "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
                },
                "first_name": {
                    "type": "string",
                    "minLength": 1
                },
                "last_name": {
                    "type": "string",
                    "minLength": 1
                }
            },
            "required": ["username", "password", "email", "first_name", "last_name"]
        }

        try:
            validate(instance=request.data, schema=schema)
        except jsonschema.ValidationError as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        user = CustomUser(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=make_password(data['password'])
        )

        user.save()

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)


class UserProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class ProductsViewSet(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        except:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
