from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegisterView, LoginView, LogoutView, UpdateProfile

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UpdateProfile.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout')
]
