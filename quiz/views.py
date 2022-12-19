from django.shortcuts import render
from .models import Lesson, QuizInstance, Question, Choices
from .serializers import QASerializer
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Avg


# Create your views here.
def home_view(request,id): 
    lesson = Lesson.objects.get(id=id) 
    response = {}
    response['id'] = lesson.id
    response['text'] = lesson.text
    response['question'] = []
    for i,question in enumerate(lesson.question_set.all()) : 
        question_instance = {}
        question_instance['id'] = question.id
        question_instance['text'] = question.text
        response['question'].append(question_instance)
        # response['question']['id'] = question.id 
        # response['question']['text'] = question.text
        # response['question']['choices']= {}
        response['question'][i]['choices'] = []
        print(response)
        for choice in question.choices_set.all(): 
            choice_instance = {}
            choice_instance['id'] = choice.id
            choice_instance['text'] = choice.text
            # response['question']['choices']['id'] = choice.id
            # response['question']['choices']['text'] = choice.text
            response['question'][i]['choices'].append(choice_instance)
           
    return JsonResponse(response)

@csrf_exempt
@api_view(['POST'])
def scoring_view(request): 
    if request.method == 'POST': 
        serializer = QASerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=serializer.validated_data['user'])
            lesson = Lesson.objects.get(id=serializer.validated_data['lesson'])
            new_quiz_instance = QuizInstance.objects.create(
                user=user,
                lesson=lesson,
                score = serializer.validated_data['score']
            )
            new_quiz_instance.save()
            return JsonResponse(serializer.validated_data)
        else : 
            return JsonResponse(serializer.errors)
    

def statistic_view(request):
    statistics = {}
    problems = Question.objects.all()
    users=User.objects.all() 
    submit_users=QuizInstance.objects.all().values_list('user')
    submissions=QuizInstance.objects.all()
    average_score = QuizInstance.objects.aggregate(Avg('score'))


    statistics['no_of_problems'] = problems.count() 
    statistics['no_of_registered_users'] = users.count()
    statistics['no_of_users_who_submit'] = len(set(submit_users))
    statistics['no_of_submissions'] = submissions.count() 
    statistics['average_score'] = average_score.get('score__avg')

    return JsonResponse(statistics)





