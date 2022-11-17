from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
import json

from .forms import CardInformation
from .models import Subscriptions, Card, Payment, UserSub

# Create your views here.

@api_view(['POST'])

def AllStudios(request):
    if request.method == 'POST':
        payload = json.loads(request.body)