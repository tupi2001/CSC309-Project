from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import CreateUserView, EditProfileView

app_name = 'accounts'

# users can register, update using their id
urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('<int:pk>/profile/edit/', EditProfileView.as_view(), name='profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
