from django.urls import path
from . import views


urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile/', views.UserProfileViewSet.as_view(), name='users-profile'),
    path('users/profile/update/', views.UserProfileViewSet.as_view(), name='users-profile-update'),
    path('users/register/', views.UserRegisterViewSet.as_view(), name='users-register'),
    path('products/', views.ProductsViewSet.as_view(), name='products'),
    path('products/<str:pk>', views.ProductViewSet.as_view(), name='product'),
    path('orders/add/', views.OrderViewSet.as_view(), name='orders-add'),
    path('orders/myorders/', views.OrderDetailsViewSet.as_view(), name='my-orders'),
    path('orders/<str:pk>/', views.OrderViewSet.as_view(), name='user-order'),
    path('orders/<str:pk>/pay/', views.OrderViewSet.as_view(), name='pay'),
    
    path('', views.hello),
]
