from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from comments.static_app_comments.serializers import UserSerializer, GroupSerializer, CommentSerializer
from comments.static_app_comments.models import Comment

class UserViewSet(viewsets.ModelViewSet):
    """
    Allows users to be viewed or edited
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    Allows groups to be viewed or edited
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    Allows users to be viewed or edited
    """
    queryset = Comment.objects.all().order_by('article_slug', 'paragraph_hash', 'timestamp')
    serializer_class = CommentSerializer

@api_view(['GET',])
def comment_list(request, slug):
    if request_method == 'GET':
        comments = Comment.objects.filter(article_slug=slug).all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

def comment_detail(request):
    if request_method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method = 'POST':
        serializer = SnippedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
