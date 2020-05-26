from django.urls import path
from . import views

app_name = "quiz"



urlpatterns = [
    path('', views.index, name="home"),
    path("get_all/", views.get_all_user_data, name="get_all"),
    path('quiz/', views.QuizList.as_view(), name="quiz_list"),
    path('quiz/<slug:slug>/', views.quiz_detail, name="quiz"),
    path('solution/<slug:slug>/', views.solution_detail, name="solution-detail"),
    path('quiz/<int:id>/data/', views.get_quiz_data, name="quiz-data"),
    path('api/quiz/<int:pk>/', views.QuizDetail.as_view(), name="quiz_detail"),
    path('api/quiz/create/', views.CreateQuiz.as_view(), name="create_quiz"),
    path('api/quiz/solution/', views.CreateSolution.as_view(), name="create_solution"),
]