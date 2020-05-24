from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserRegisterSerializer
from rest_framework import status
from . import forms
User = get_user_model


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {'user': request.user})


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully registered a new user"
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == "POST":
        user_form = forms.UserCreationForm(request.POST, files=request.FILES)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            messages.success(request, f'Account {user.username} created successfully')
    else:
        user_form = forms.UserCreationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})