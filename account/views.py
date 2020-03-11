from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {'user': request.user})