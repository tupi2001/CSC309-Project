from django.urls import path

from .views import StudioInformationView, ListDistanceView, AllStudioInfoView

app_name = 'studios'

# user can look for the info of a specific studio, or list all studios by which is closer or
# search for a specific studio
urlpatterns = [
    path('<int:studio_id>/info/', StudioInformationView.as_view(), name='studio_information'),
    path('allstudios/', ListDistanceView.as_view()),
    path('search/',AllStudioInfoView.as_view()),
]
