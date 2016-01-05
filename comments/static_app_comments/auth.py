from rest_framework import authentication
from rest_framework import exceptions
from comments.static_app_comments.models import Commenter
from rest_framework import permissions
import requests

def login_commenter(access_token):
    commenter_data = requests.get('https://api.github.com/user', headers = {
        'Accept': 'application/json',
        'Authorization': "token {}".format(access_token)
    }).json()
    if Commenter.objects.filter(login=commenter_data['login']).exists():
        commenter = Commenter.objects.get(login=commenter_data['login'])
        commenter.email = commenter_data['email']
        commenter.avatar_url = commenter_data['avatar_url']
        commenter.name = commenter_data['name']
        commenter.token = access_token
        commenter.save()
    else:
        commenter = Commenter.objects.create(
            login = commenter_data['login'],
            email = commenter_data['email'],
            avatar_url = commenter_data['avatar_url'],
            name = commenter_data['name'],
            token = access_token
        )
    return commenter

class GithubPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.META.get('HTTP_AUTHORIZATION'):
                token = request.META.get('HTTP_AUTHORIZATION').split('token ')[1]
                try:
                    #We are doing both authentication and authorization here.
                    #This is not really the proper way to do this.
                    commenter = Commenter.objects.get(token=token,
                        login=request.data['commenter']['login'])
                    if commenter.banned:
                        return False
                    if request.data['commenter'].get('name') != commenter.name or \
                        request.data['commenter'].get('avatar_url') != commenter.avatar_url:
                        commenter = login_commenter(token) #refresh the commenter's data
                    return True
                except Commenter.DoesNotExist:
                    return False
            else:
                return False
