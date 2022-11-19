from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from subscriptions.views import AddCard, AddSubscription, UpdateCard, UpdateSubscription, PaymentHistory

app_name = 'subscriptions'

urlpatterns = [
    path('addcard/', AddCard.as_view(), name='addcard'),
    path('updatecard/', UpdateCard.as_view(), name='updatecard'),
    path('addsub/', AddSubscription.as_view(), name='addsub'),
    path('updatesub/', UpdateSubscription.as_view(), name='updatesub'),
    path('paymenthistory/', PaymentHistory, name='paymenthistory'),
]