from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from subscriptions.views import AddCard, AddSubscription, UpdateCard, UpdateSubscription, PaymentHistory, SubscriptionsViewSet, CardViewSet, UserSubViewSet

app_name = 'subscriptions'

# user can add or update their card, add or update their current subscription
# and look at their payment history

urlpatterns = [
    path('addcard/', AddCard.as_view(), name='addcard'),
    path('updatecard/<int:pk>/', UpdateCard.as_view(), name='updatecard'),
    path('addsub/', AddSubscription.as_view(), name='addsub'),
    path('showcard/', CardViewSet.as_view(), name='showcard'),
    path('showsubs/', SubscriptionsViewSet.as_view(), name='showsubs'),
    path('showsub/', UserSubViewSet.as_view(), name='showsub'),
    path('updatesub/<int:pk>/', UpdateSubscription.as_view(), name='updatesub'),
    path('paymenthistory/', PaymentHistory.as_view(), name='paymenthistory'),
]