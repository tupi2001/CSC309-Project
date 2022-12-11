from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken import views
from accounts.views import CreateUserView, EditProfileView, UserViewSet

app_name = 'accounts'

# users can register, update using their id
urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('<int:pk>/profile/edit/', EditProfileView.as_view(), name='profile'),
    path('me/', UserViewSet.as_view(), name='me'),
    path('api/token/', views.obtain_auth_token, name='token_obtain_pair'),
]
