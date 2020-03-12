from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404
from .models import Quiz, Answer, Question, Solution
import json
from .permissions import IsOwnerOrReadOnly
from .serializers import AnswerSerializer, QuizSerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer, SolutionSerializer
# Create your views here.

@api_view(["GET"])
def get_all_user_data(request):
    if request.user.is_authenticated:
        data = {
            'username': request.user.username,
            'email': request.user.email,
            'quizes': [quiz.to_json() for quiz in Quiz.objects.all()],
            'solutions': [solution.to_json for solution in Solution.objects.filter(user=request.user)]
        }
        return Response(data)
    return Response(status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)

class QuizList(generics.ListCreateAPIView):
    
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    

class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    permissions = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class CreateQuiz(generics.CreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request):
        r_data = request.data
        data = {
            'user': request.user.pk,
            'title': r_data.get('title'),
            'score_for_each_question': r_data.get("time_for_each_question"),
            'pass_mark': r_data.get('pass_mark'),
            'time_for_each_question': r_data.get('time_for_each_question'),
        }
        quiz_serializer = QuizSerializer(data=data)
        if quiz_serializer.is_valid():
            quiz = quiz_serializer.save()
            for question in r_data.get('questions'):
                data = {
                    "question": question.get("question"),
                    "quiz": quiz.id,
                }
                serializer = QuestionSerializer(data=data)
                if serializer.is_valid():
                    que = serializer.save()
                    for answer in question.get('answers'):
                        data = {
                            "question": que.id,
                            "answer": answer.get("answer"),
                            "is_correct": answer.get("is_correct"),
                        }
                        serializer = AnswerSerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(quiz_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerList(generics.ListCreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Answer.objects.filter(question_id=self.kwargs["pk"])
        return queryset


class CreateSolution(generics.CreateAPIView):
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        r_data = request.data
        user = request.user.pk
        data = {
            'user': user,
            'quiz': r_data.get('quiz'),
            'score': r_data.get("score"),
        }
        solution_serializer = SolutionSerializer(data=data)
        if solution_serializer.is_valid():
            solution = solution_serializer.save()
            for choice in r_data.get('choice'):
                data = {
                    "user": user,
                    "question": choice.get("question"),
                    "solution": solution.id,
                    "score": choice.get("score"),
                    "answer": choice.get('answer'),
                    'time_taken': choice.get("time_taken")
                    
                }
                serializer = ChoiceSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(solution_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
