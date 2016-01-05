from django.test import TestCase
import pytest
from comments.static_app_comments.models import Comment

# Create your tests here.

from rest_framework.test import APIClient

@pytest.mark.django_db
def test_save_comment():
    client = APIClient()
    response = client.post('/comments/', {
        'article_url': 'http://0.0.0.0:8080/saltstack-from-scratch',
        'user': {
            'login': 'amfarrell',
            'email': 'af@jambonsw.com',
            'name': 'Andrew Farrell',
            'avatar_url': "https://avatars.githubusercontent.com/u/123831?v=3",
        },
        'comment_hash': 1242837,
        'paragraph_hash': 1242897,
        'deleted': False,
        'text': "I see a little siluetto of a man.",
    }, format='json')
    assert 201 == response.status_code
    assert Comment.objects.get(user_email = 'af@jambonsw.com')

@pytest.mark.django_db
def test_get_comments():
    commenter_data = {
        'login': 'amfarrell',
        'email': 'af@jambonsw.com',
        'name': 'Andrew M. Farrell',
        'avatar_url': "https://avatars.githubusercontent.com/u/123831?v=3",
    }
    Commenter.objects.create()
    comment_data = {
        'article_url': 'http://0.0.0.0:8080/saltstack-from-scratch',
        'paragraph_hash': 1242897,
        'comment_hash': 1242837,
        'deleted': False,
        'text': "I see a little siluetto of a man.",
    }
    Comment.objects.create(**comment_data)
    client = APIClient()
    response = client.get('/comments/', format='json')
    assert 1 == len(response.data)
    assert response.data[0].get('timestamp')
    assert response.data[0].get('user_email') == comment_data['user_email']
    assert response.data[0].get('paragraph_hash') == comment_data['paragraph_hash']
    assert response.data[0].get('user_name') == comment_data['user_name']
