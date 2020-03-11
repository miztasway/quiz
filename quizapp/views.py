from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Quiz
import json
# Create your views here.

@login_required
def quiz(request, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    if quiz.user_answered(request.user):
        return HttpResponse("<h1>You have answered the quiz</h1>")
    quiz_json = json.dumps(quiz.to_json())
    return render(request, 'quiz/quiz.html', {'quiz': quiz,'quiz_json': quiz_json})