from django.urls import path

from .views import StudioInformationView, ListDistanceView, AllStudioInfoView

app_name = 'studios'

urlpatterns = [
    path('<int:studio_id>/info/', StudioInformationView.as_view(), name='studio_information'),
    path('allstudios/', ListDistanceView.as_view()),
    path('search/',AllStudioInfoView.as_view()),
]
