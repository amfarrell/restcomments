import requests
import requests.auth
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from comments.static_app_comments.serializers import \
    UserSerializer, CommentSerializer
from comments.static_app_comments.models import Comment

class UserViewSet(viewsets.ModelViewSet):
    """
    Allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Allows users to be viewed or edited
    """
    queryset = Comment.objects.all().order_by('article_url', 'paragraph_hash', 'timestamp')
    serializer_class = CommentSerializer
    permission_classes = [GithubPermission]


@api_view(['GET'])
def get_token(request, code):
    token_response = requests.post(settings.TOKEN_URL, data = {
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'code': code,
    }, headers = {
        'Accept': 'application/json'
    })
    token_json = github_response.json()
    return JsonResponse(github_response.json())

@api_view(['GET', 'POST'])
def comment_list(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        print(request.data)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def comment_detail(request):
    if request_method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SnippedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
