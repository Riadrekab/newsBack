import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.validators import validate_email
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError
from .serializers import UserSerializer, ProfileSerializer, TopicSerializer, ResultSerializer
from users.models import Profile, Topic, Result,historyResult
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.http import HttpResponse,JsonResponse
from django.conf import settings

from eventregistry import *

import torch

import json

from scipy.special import softmax

import time

from flask import Flask, jsonify, request

import json


import requests

import json

import os


TARGET_NAMES = ['World', 'Sports', 'Business', 'Sci/Tech'] 

er = EventRegistry(apiKey='62fd2d2a-c90f-4cc1-9b72-ad5f85739368')

def replace_element(lst, old_element, new_element):
    for i in range(len(lst)):
        if lst[i] == old_element:
            lst[i] = new_element
    return lst

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'POST': 'api/users/login/'},
        {'POST': 'api/users/login/refresh/'},
        {'POST': 'api/users/register/'},
        {'GET': 'api/users/valid-token/'},
        {'GET': 'api/users/logout/blacklist/'},
        {'GET': 'api/users/<str:username>/'},
        {'POST': 'api/users/update/<str:username>/'},
        {'GET': 'api/topics/'},
        {'GET': 'api/topics/<str:username>/'},
    ]
    return Response(routes)


@api_view(['POST'])
def registerUser(request):
    data = request.data

    # Validate the user input.
    if not data['first_name']:
        return Response({'detail': 'First name is required.'}, status=400)
    if not data['last_name']:
        return Response({'detail': 'Last name is required.'}, status=400)
    if not data['username']:
        return Response({'detail': 'Username is required.'}, status=400)
    if User.objects.filter(username=data['username']).exists():
        return Response({'detail': 'Username not available.'}, status=400)
    try:
        validate_email(data['email'])
    except ValidationError:
        return Response({'detail': 'Please enter a valid email address.'}, status=400)
    if User.objects.filter(email=data['email']).exists():
        return Response({'detail': 'User with this email already exists.'}, status=400)
    if not data['password']:
        return Response({'detail': 'Password is required.'}, status=400)
    if not data['password_confirmation']:
        return Response({'detail': 'Please confirm your password.'}, status=400)
    if data['password'] != data['password_confirmation']:
        return Response({'detail': 'Passwords do not match.'}, status=400)

    # Hash the user password.
    password = data['password']
    user = User.objects.create_user(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        email=data['email'],
        password=password
    )
    user.set_password(password)
    user.save()

    return Response('User was created')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def decode_token(token):
    payload = jwt.decode(token, algorithms="HS256", key=settings.SECRET_KEY)
    return payload


@api_view(['GET'])
def validate_token(request):
    token = request.GET.get('access')
    try:
        payload = decode_token(str(token))
        user = User.objects.get(id=payload['user_id'])
        return Response({'detail': 'Token is valid', 'username': user.username, 'valid': True}, status=200)
    except:
        return Response({'detail': 'Token is invalid', 'valid': False}, status=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    return Response(ProfileSerializer(profile, many=False).data)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def updateProfile(request, username):
    # if request.user.username != username:
    #     return Response({'detail': 'You do not have permission to edit this profile.', 'user': request.user.username}, status=401)

    # profile = get_object_or_404(Profile, user=request.user)

    user = Profile.objects.filter(username=request.data['username']).first()

    # update basic info
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.username = request.data.get('username', user.username)
    user.email = request.data.get('email', user.email)

    # update preferred topics

    preferred_topic_ids = request.data.get('preferred_topics', [])
    preferred_topics = Topic.objects.filter(id__in=preferred_topic_ids)
    user.preferred_topics.set(preferred_topics)

    user.save()

    return Response({'detail': 'Profile updated successfully.', 'profile': ProfileSerializer(user, many=False).data},
                    status=200)


@api_view(['GET'])
def getTopics(request):
    topics = Topic.objects.all()
    return Response(TopicSerializer(topics, many=True).data)


@api_view(['GET'])
def getProfileTopics(request, username):
    profile = get_object_or_404(Profile, username=username)
    topics = profile.preferred_topics.all()
    return Response(TopicSerializer(topics, many=True).data)


@api_view(['GET'])
def savedResults(request, username):
    user = User.objects.get(username=username)
    results = user.profile.result_set.all()
    return Response(ResultSerializer(results, many=True).data)


@api_view(['POST'])
def saveResult(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    result = Result.objects.create(
        profile=profile,
        title=request.data['title'],
        body=request.data['body'],
        url=request.data['url'],
        image=request.data['image'],
    )
    return Response(ResultSerializer(result, many=False).data)


@api_view(['DELETE'])
def deleteResult(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    result = profile.result_set.get(id=request.data['id'])
    result.delete()
    return Response('Result deleted')


class getNews(APIView):

    def get(self, request):
        inputUser = request.GET.get('input')
        print(inputUser)
        q = QueryArticlesIter(
            # keywords=QueryItems.OR(["Elon Musk", "Messi"]),
            keywords=inputUser,
            keywordsLoc="body",
            ignoreKeywords="SpaceX",
            dateStart='2023-01-01',
            dateEnd='2023-04-30',
            # lang='fra',
            lang = 'eng',
        )
        listAr = []
        listAr = [article for article in q.execQuery(er, sortBy="rel", returnInfo=ReturnInfo(
            articleInfo=ArticleInfoFlags(concepts=True, categories=True)), maxItems=50)]
        json_response = json.dumps(listAr, indent=4)
        print(json_response)
        return Response(json_response)


def getCategoriesFromUserName(username):
    profile = get_object_or_404(Profile, username=username)
    topics = profile.preferred_topics.all()
    listTopics = []
    listTopics = [item.category.name for item in topics]
    return listTopics



@api_view(['GET'])
def getFeatured(request, username):
    input = username
    user = Profile.objects.filter(username=input).first()
    q = QueryArticlesIter(
        keywords= '',

        # keywords=QueryItems.OR(getCategoriesFromUserName(user.username)),
        # keywords= input,
        keywordsLoc="body",
        # ignoreKeywords="SpaceX",
        dateStart='2023-01-01',
        # dateEnd='2023-04-30',
        # lang='fra',
        lang='eng',
    )
    listAr = []
    # Check if article matches 
    listAr = [article for article in q.execQuery(er, sortBy="rel", returnInfo=ReturnInfo(
        articleInfo=ArticleInfoFlags(concepts=True, categories=True)), maxItems=100)]
    listIds = list(range(1, len(listAr) + 1))
    listAr2 = [item['body'] for item in listAr]
    vals = make_predictions(listAr2,listIds)
    classes = [item['predicted_class'] for item in vals]
    savedTexts = []
    i = 0    
    listUserClasses = getCategoriesFromUserName(user.username) 
    listUserClasses = replace_element(listUserClasses, "Technology", "Sci/Tech")
    listUserClasses = replace_element(listUserClasses, "Careers", "Business")
    listUserClasses = replace_element(listUserClasses, "Brands", "World")


    print(listUserClasses)
    print("ohuhu")
    while (i< len(classes)):
        if(any(element in  listUserClasses for element in classes[i] )   ):
            savedTexts.append(listAr[i])
        i +=1
    json_response = json.dumps(savedTexts, indent=4)
    return Response(json_response)



class saveHistory(APIView) : 
    def post(self,request):
        user = User.objects.get(username = request.data['username'])
        profile = user.profile
        res = historyResult.objects.create(
            profile = profile,
            input = request.data['search']
        )
        return JsonResponse('Done',safe=False)
    


        
@api_view(['GET'])
def getHistory(request,username):
    profil = Profile.objects.filter(username=username).first()
    res = historyResult.objects.filter(profile= profil).all()
    inputs = []
    inputs = [item.input for item in res]
    return JsonResponse(inputs, safe=False)
    
    
model = torch.load("../saved_model_bert_uncased_L-2_H-128_A-2") 


def make_predictions(texts_list, ids_list, extras_list=()):

    # """

    # Predict output classes from text documents

    # :param texts_list: list of text documents

    # :param ids_list: lists of the ids of the text documents

    # :param extras_list: lists of the extra attributes of each text document as dictionaries

    # :return: A list of dictionaries each containing the document id, text content, extra attributes and a list for the

    #             predicted classes

    # """
    preds, raw_outputs = model.predict(texts_list)  # Predict from DL model

    probabilities = softmax(raw_outputs, axis=1)
  
    predicted_classes = []

 

    # For each prediction find the corresponding class(es)

    for index, probs in enumerate(probabilities):

        classes_indexes = []

        for pos, prob in enumerate(probs):

            # If the probability is >= to the 1/number_of_classes

            # then the corresponding class is significant enough to be considered

            if prob >= 1.0/float(len(TARGET_NAMES)):

                classes_indexes.append((prob, pos))

        # Sort infered classes with respect to decreasing probabilities

        classes_indexes.sort(key= lambda x: x[0], reverse=True)

        classes = [TARGET_NAMES[p[1]] for p in classes_indexes]

        predicted_classes.append(classes)

 

    print(predicted_classes)

 

    predictions_json = []

    # Format the predictions before returning

    for index in range(0, len(texts_list)):

        _p = {

            "id": ids_list[index],

            # "predicted_class": TARGET_NAMES[preds[index]],

            "predicted_class": predicted_classes[index],

            "text": texts_list[index]

        }

        if extras_list:

            extra_data = extras_list[index]

            if extra_data:

                for k, v in extra_data.items():

                    _p[k] = v

        predictions_json.append(_p)

    return predictions_json


# text2 = "MYSTERY lab in Wuhan conducted secret experiments to clone and soup up coronaviruses to infect humans, a bombshell study has revealed. For the last three years, a group of scientists have been combing through online databases and other sources of evidence for vital clues about the origins of Covid. "
# text1 = "FC Barcelona won the Spanish championanship by 14 points from it's eternal rival Real Madrid after a record breaking season for the spanish giant"

# text_lists = [text1,text2]
# ids = [1,2]
# print(make_predictions(text_lists,ids))



@api_view(['GET'])
def predictTopic(request):
    text2 = "PART OF what makes HBO's Succession so great is that each and every character in the show -- for better and for worse -- feels completely, 100% like a real person. And that leads to situations that feel like real situations. And moments that feel like real moments. And when something like that is fleshed out so strongly, it can lead to revelations we never thought we would see, such as four of Logan Roy's previous wives and mistresses sitting together in unity at his funeral. Such was one of many memorable scenes in Season 4, Episode 9, Church and State. Maybe the fact that it was only after he was finally gone that four specific people who were once close to the miserable Logan ca "
    text1 = "FC Barcelona won the Spanish championanship by 14 points from it's eternal rival Real Madrid after a record breaking season for the spanish giant. The catalan football club has made huge progress this year, scoring 110 goals and conceeding only 10"
    text_lists = [text1,text2]
    ids = [1,2]
    print(make_predictions(text_lists,ids))
