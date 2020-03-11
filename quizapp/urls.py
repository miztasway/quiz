from django.urls import path
from . import views

app_name = "quiz"



urlpatterns = [
    path('quiz/<slug:quiz_slug>/', views.quiz, name="quiz"),
]