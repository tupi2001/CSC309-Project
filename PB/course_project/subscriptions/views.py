from django.shortcuts import render
from django.views.generic import FormView, ListView

from .forms import CardInformation
from .models import Subscriptions, Card, Payments, UserSub

# Create your views here.

class SubscriptionViews(ListView):
    model = Subscriptions
    # template = 

    def get_subscription(self):
        curr_user = self.request.user

        user_member = UserSub.objects.filter(user=curr_user)

        if user_member.exists():
            return user_member.subscription
        else:
            return None

class Payment(FormView):
    form_class = CardInformation

    def form_valid(self, form):
        current_user = self.request.user

        