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
            'description': r_data.get('description'),
            'score_for_each_question': r_data.get("score_for_each_question"),
            'pass_mark': r_data.get('pass_mark'),
            'time_for_each_question': r_data.get('time_for_each_question'),
        }
        quiz_instance = None
        if (r_data.get('id')):
            quiz_instance = get_object_or_404(Quiz, id=r_data.get('id'), user=request.user)
            for question in quiz_instance.questions.all():
                question.delete()

        quiz_serializer = QuizSerializer(data=data, instance=quiz_instance)

        if quiz_serializer.is_valid():
            
            quiz = quiz_serializer.save()
            for question in r_data.get('questions'):
                question_instance = None
                if (question.get('id')):
                    question_query = quiz.questions.filter(id=int(question.get('id')))
                    if question_query.exists():
                        question_instance = question_query[0]
                
                data = {
                    "question": question.get("question"),
                    "quiz": quiz.id,
                }
                question_serializer = QuestionSerializer(data=data, instance=question_instance)
                if question_serializer.is_valid():
                    que = question_serializer.save()
                    for answer in question.get('answers'):
                        answer_instance = None
                        if (answer.get('id')):
                            answer_query = que.answers.filter(id=int(answer.get('id')))
                            if answer_query.exists():
                                answer_instance = answer_query[0]
                        
                        data = {
                            "question": que.id,
                            "answer": answer.get("answer"),
                            "is_correct": answer.get("is_correct"),
                        }
                        answer_serializer = AnswerSerializer(data=data)
                        if answer_serializer.is_valid():
                            answer_serializer.save()
                        else:
                            
                            return Response(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    quiz.delete()
                    return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            data = {
                'quiz_url': quiz.get_absolute_url(),
                'id': quiz.id,
                'title': quiz.title,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(quiz_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        quiz = get_object_or_404(Quiz, id=int(r_data.get('quiz')))
        solution_query = quiz.solutions.filter(user=request.user)
        if solution_query.exists():
            for solution in solution_query:
                solution.delete()
            
        
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
                    solution.delete()
                    print('Error occured here', serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            solution.save()
            if request.GET.get('redirect'):
                redirect('quiz:solution-detail', kwargs={'slug': solution.quiz.slug})
            return Response(SolutionSerializer(solution).data, status=status.HTTP_201_CREATED)

        else:
            print('Error occured 3', solution_serializer.errors)
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
def create_quiz(request, pk=None):
    if pk:
        quiz = get_object_or_404(Quiz, id=pk, user=request.user)
    else:
        quiz = None

    return render(request, 'quiz/create_quiz.html', {'quiz': quiz})

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

@api_view(['GET'])
def get_quiz_by_slug(request):
    slug = request.GET.get('slug')
    if slug:
        quiz_query = Quiz.objects.filter(slug=slug)
        if quiz_query.exists():
            data = {
                "Found": True,
                'url': quiz_query[0].get_absolute_url()
            }
        else:
            data = {
                'Found': False,
                'error_message': f'{slug} did not match any quiz',
            }
    else:
        data = {
            "Found": False,
            'error_message': "A slug must be provided"
        }
    return Response(data)

@api_view(['GET'])
def delete_question(request, id):
    question = get_object_or_404(Question, id=id)
    if question.quiz.user == request.user:
        question.delete()
        return Response({'completed': True}, status=status.HTTP_200_OK)
    return Response({'completed': False, 'message': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
    