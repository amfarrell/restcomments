from django.test import TestCase
import pytest
from comments.static_app_comments.models import Comment, Commenter

# Create your tests here.

from rest_framework.test import APIClient

@pytest.mark.django_db
def test_save_comment():
    test_token = 'token fjkdls0u4089riopjwirf'
    commenter_data = {
        'login': 'amfarrell',
        'email': 'af@jambonsw.com',
        'name': 'Andrew M. Farrell',
        'avatar_url': "https://avatars.githubusercontent.com/u/123831?v=3",
        'token': test_token.split('token ')[1],
    }
    commenter = Commenter.objects.create(**commenter_data)
    client = APIClient()
    response = client.post('/comments/', {
        'article_url': 'http://0.0.0.0:8080/saltstack-from-scratch',
        'commenter': commenter_data,
        'comment_hash': 1242837,
        'paragraph_hash': 1242897,
        'deleted': False,
        'text': "I see a little siluetto of a man.",
    }, format='json', HTTP_AUTHORIZATION=test_token)
    assert 201 == response.status_code
    assert Comment.objects.get(commenter__email = commenter_data['email'])

@pytest.mark.django_db
def test_dont_save_comment_if_token_mismatches():
    test_token = 'token fjkdls0u4089riopjwirf'
    commenter_data = {
        'login': 'amfarrell',
        'email': 'af@jambonsw.com',
        'name': 'Andrew M. Farrell',
        'avatar_url': "https://avatars.githubusercontent.com/u/123831?v=3",
        'token': test_token.split('token ')[1],
    }
    commenter = Commenter.objects.create(**commenter_data)
    client = APIClient()
    response = client.post('/comments/', {
        'article_url': 'http://0.0.0.0:8080/saltstack-from-scratch',
        'commenter': commenter_data,
        'comment_hash': 1242837,
        'paragraph_hash': 1242897,
        'deleted': False,
        'text': "I see a little siluetto of a man.",
    }, format='json', HTTP_AUTHORIZATION=test_token+'sabot')
    assert 403 == response.status_code
    assert 0 == Comment.objects.filter(commenter__email = commenter_data['email']).count()

@pytest.mark.django_db
def test_get_comments():
    test_token = 'fjkdls0u4089riopjwirf'
    commenter_data = {
        'login': 'amfarrell',
        'email': 'amfarrell@mit.edu',
        'name': 'Andrew M. Farrell',
        'avatar_url': "https://avatars.githubusercontent.com/u/123831?v=3",
        'token': test_token,
    }
    commenter = Commenter.objects.create(**commenter_data)
    comment_data = {
        'article_url': 'http://0.0.0.0:8080/saltstack-from-scratch',
        'paragraph_hash': 1242897,
        'comment_hash': 1242837,
        'deleted': False,
        'text': "I see a little siluetto of a man.",
        'commenter': commenter
    }
    Comment.objects.create(**comment_data)
    client = APIClient()
    response = client.get('/comments/', format='json')
    assert 1 == len(response.data)
    assert response.data[0].get('timestamp')
    assert response.data[0].get('commenter').get('email') == commenter_data['email']
    assert response.data[0].get('paragraph_hash') == comment_data['paragraph_hash']
    assert response.data[0].get('commenter').get('name') == commenter_data['name']
