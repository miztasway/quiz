from django.urls import path
from . import views

app_name = "quiz"



urlpatterns = [
    path('quiz/', views.QuizList.as_view(), name="quiz_list"),
    path('quiz/<int:pk>/', views.QuizDetail.as_view(), name="quiz"),
    
]