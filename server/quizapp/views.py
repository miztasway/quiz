from django.shortcuts import render, get_object_or_404, redirect
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404
from django.core.paginator import Paginator
from .models import Quiz, Answer, Question, Solution
import json
import datetime
from .permissions import IsOwnerOrReadOnly
from .serializers import AnswerSerializer, QuizSerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer, SolutionSerializer, SolutionCreateSerializer
from .models import Quiz
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
            'time_for_each_question': r_data.get("time_for_each_question"),
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
        print(r_data['score'], 'score was \n\n')
        user = request.user.pk
        
        data = {
            'user': user,
            'quiz': r_data.get('quiz'),
            'score': r_data.get("score"),
        }
        quiz = get_object_or_404(Quiz, id=int(r_data.get('quiz')))
        solution_query = quiz.solutions.filter(user=request.user)
        if not solution_query.exists():
            data['id'] = solution_query[0]
            for choice in solution.choices.all():
                choice.delete()
        
        solution_serializer = SolutionCreateSerializer(data=data)
        if solution_serializer.is_valid():
            solution = solution_serializer.save()
            for choice in r_data.get('choices'):

                data = {
                    "user": user,
                    "question": choice["question"],
                    "solution": solution.id,
                    "score": choice["score"],
                    "answer": choice['answer'],
                    'time_taken': datetime.timedelta(seconds=int(choice["time_taken"]))
                    
                }
                serializer = ChoiceSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print('I raised the errors 1')
                    solution.delete()
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            solution.save()
            if request.GET.get('redirect'):
                redirect('quiz:solution-detail', kwargs={'slug': solution.quiz.slug})
            return Response(SolutionSerializer(solution).data, status=status.HTTP_201_CREATED)

        else:
            print("I raised the errors 2")
            return Response(solution_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def index(request):
    quizzes = Quiz.objects.all()
    page = int(request.GET.get('page', 0))
    paginator = Paginator(quizzes, 12)
    if page > paginator.num_pages:
        page = paginator.num_pages
    elif page < 0:
        page = 0
    quizzes = paginator.get_page(page)
    return render(request, 'quiz/index.html', {'quizzes': quizzes})

@login_required
def create_quiz(request):
    return render(request, 'quiz/create_quiz.html', {})
@login_required
def quiz_detail(request, slug):
    quiz = get_object_or_404(Quiz, slug=slug)
    solution_query = quiz.solutions.filter(user=request.user)
    solution = None
    if  solution_query.exists():
        solution = solution_query[0]
    return render(request, 'quiz/quiz.html', {'quiz': quiz, 'solution': solution})

@login_required
@api_view(["GET"])
def get_quiz_data(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    return Response(quiz.to_json())
