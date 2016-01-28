import requests
import requests.auth
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.conf import settings
from comments.static_app_comments.serializers import CommentSerializer
from comments.static_app_comments.models import Comment

from comments.static_app_comments.serializers import CommentSerializer
from comments.static_app_comments.models import \
    Comment, Commenter
from comments.static_app_comments.auth import GithubPermission, login_commenter

import logging
logger = logging.getLogger('django')

class CommentViewSet(viewsets.ModelViewSet):
    """
    Allows comments to be viewed or edited
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

    if requests.codes.ok != token_response.status_code:
        logger.error("Request to github returned {}".format(token_response.status_code))
        logger.error(token_response.text)

    token_json = token_response.json()
    if token_json.get('access_token'):
        login_commenter(token_json['access_token'])
    return JsonResponse(token_response.json())
