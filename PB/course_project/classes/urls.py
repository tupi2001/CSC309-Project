from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from classes.views import CreateClassView, UpdateClassView, DeleteClassView, ClassesView, UserClassesView
from classes.views import EnrolUserInClassView, RemoveUserFromClassesView, RemoveUserFromClassView
from classes.views import DeleteClassesView

app_name = 'classes'

urlpatterns = [
    path('create/', CreateClassView.as_view(), name='create'),
    path('<int:class_id>/update/', UpdateClassView.as_view(), name='update'),
    path('<int:class_id>/delete/', DeleteClassView.as_view(), name='delete'),
    path('<int:class_id>/delete/all/', DeleteClassesView.as_view(), name='delete'),
    path('<int:studio_id>/view/', ClassesView.as_view(), name='view'),
    path('user/enrol/<int:class_id>/', EnrolUserInClassView.as_view(), name='view'),
    path('user/unenrol/<int:class_id>/', RemoveUserFromClassView.as_view(), name='view'),
    # path('<int:user_id>/enrol/<int:studio_id>/', ClassesView.as_view(), name='view')
    path('user/unenrol/<int:studio_id>/', RemoveUserFromClassesView.as_view(), name='view'),
    path('user/view/', UserClassesView.as_view(), name='view'),
]