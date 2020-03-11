from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from . import views
app_name = "account"

urlpatterns = [
    path('login/',LoginView.as_view(), name="login"),
    path('logout/',LogoutView.as_view(), name="logout"),
    path('', views.dashboard, name="dashboard")
]