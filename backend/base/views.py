from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .models import Product, CustomUser, Order, OrderItem, ShippingAddress
from .serializers import ProductSerializer, OrderSerializer
from jsonschema import validate
import jsonschema
from datetime import datetime
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

    def put(self, request):
        user = request.user
        serializer = UserSerializerWithToken(user, many=False)

        data = request.data

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        if data['password'] != '':
            user.password = make_password(data['password'])

        user.save()

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


class OrderViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        order_items = data['orderItems']

        if order_items and len(order_items) == 0:
            return Response({'detail':'No order items'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            #1 Create Order
            order = Order.objects.create(
                user=user,
                payment_method=data['paymentMethod'],
                shipping_price=data['shippingPrice'],
                total_price=data['totalPrice']
            )

            #2 Create shipping address
            shipping = ShippingAddress.objects.create(
                user=user,
                order=order,
                address=data['shippingAddress']['address'],
                city=data['shippingAddress']['city'],
                postal_code=data['shippingAddress']['postalCode'],
                country=data['shippingAddress']['country']
            )

            #3 Create order items and set order to orderItem relationship
            for i in order_items:
                product = Product.objects.get(id=i['product'])

                item = OrderItem.objects.create(
                    name=product.name,
                    product=product,
                    order=order,
                    quantity=i['qty'],
                    image=product.image.url
                )

            #4 Update stock
                product.count_in_stock -= item.quantity
                product.save()

            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
    
    def get(self, request, pk):
        user = request.user

        try:
            order = Order.objects.get(id=pk)
            if user.is_staff or order.user == user:
                serializer = OrderSerializer(order, many=False)
                return Response(serializer.data)
            else:
                Response({'detail':'Not authorized to view this order'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'detail':'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        order = Order.objects.get(id=pk)

        order.is_paid = True
        order.paid_at = datetime.now()
        order.save()
        
        return Response('Order was paid')

class OrderDetailsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = user.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)