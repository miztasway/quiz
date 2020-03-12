from django.urls import path
from . import views

app_name = "quiz"



urlpatterns = [
    path("get_all/", views.get_all_user_data, name="get_all"),
    path('quiz/', views.QuizList.as_view(), name="quiz_list"),
    path('quiz/<int:pk>/', views.QuizDetail.as_view(), name="quiz_detail"),
    path('quiz/create/', views.CreateQuiz.as_view(), name="create_quiz"),
    path('quiz/solution/', views.CreateSolution.as_view(), name="create_solution"),
]