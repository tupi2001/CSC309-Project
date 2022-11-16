"""course_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import RegisterView, LoginView, LogoutView
from classes.views import CreateClassView, UpdateClassView, DeleteClassView, DeleteClassesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create-class/', CreateClassView.as_view(), name='create-class'),
    path('update-class/', UpdateClassView.as_view(), name='update-class'),
    path('delete-class/', DeleteClassView.as_view(), name='delete-class'),
    path('delete-classes/', DeleteClassesView.as_view(), name='delete-classes')
]
