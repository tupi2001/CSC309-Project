from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

<<<<<<< HEAD
from accounts.views import RegisterView, LoginView, LogoutView
=======
from accounts.views import RegisterView, LoginView, LogoutView, UpdateProfile
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
<<<<<<< HEAD
    path('logout/', LogoutView.as_view(), name='logout')
]
=======
    path('profile/', UpdateProfile.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout')
]
>>>>>>> 50a7af8f06d3a7344799114325fdbcff1fbb1e18
