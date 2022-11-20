from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from classes.views import CreateClassView, UpdateClassView, DeleteClassView, ClassesView

app_name = 'classes'

urlpatterns = [
    path('create-class/', CreateClassView.as_view(), name='create'),
    path('update/', UpdateClassView.as_view(), name='update'),
    path('delete-class/', DeleteClassView.as_view(), name='delete_class'),
    path('view-classes', ClassesView.as_view(), name='view-classes')
]