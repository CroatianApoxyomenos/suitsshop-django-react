from django.urls import path
from . import views


urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile/', views.UserProfileViewSet.as_view(), name='users-profile'),
    path('users/register/', views.UserRegisterViewSet.as_view(), name='users-register'),
    path('products/', views.ProductsViewSet.as_view(), name='products'),
    path('products/<str:pk>', views.ProductViewSet.as_view(), name='product'),
    path('', views.hello),
]
