from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Quiz
import json
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer, SolutionSerializer
# Create your views here.

@login_required
def quiz(request, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    if quiz.user_answered(request.user):
        return HttpResponse("<h1>You have answered the quiz</h1>")
    quiz_json = json.dumps(quiz.to_json())
    return render(request, 'quiz/quiz.html', {'quiz': quiz,'quiz_json': quiz_json})


class QuizList(APIView):
    def get(self, request):
        quizes = Quiz.objects.all()
        data = QuizSerializer(quizes, many=True).data
        return Response(data)
    

class QuizDetail(APIView):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        data = QuestionSerializer(quiz).data
        return Response(data)