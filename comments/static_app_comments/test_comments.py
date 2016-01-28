import pytest
from datetime import datetime, timedelta

from django.test import TestCase
from django.core import mail
from django.core.management import call_command

from rest_framework.test import APIClient

from comments.static_app_comments.models import Comment, Commenter

#For now, these tests are very integrationey.

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
        'text': "32,000 troops in New York Harbor.",
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
        'text': "I will send a fully-armed battalion to remind you of my love.",
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
        'text': "Talk less; Smile More.",
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

@pytest.mark.django_db
def test_email_comments():
    test_token = 'fjkdls0u4089riopjwirf'
    commenter_data = {
        'login': 'amfarrell',
        'email': 'amfarrell@mit.edu',
        'name': 'Andrew M. Farrell',
        'avatar_url': "https://avatars.githubusercontent.com/u/123831?v=3",
        'token': test_token,
    }
    commenter = Commenter.objects.create(**commenter_data)
    new_comment_data = {
        'article_url': 'http://0.0.0.0:8080/saltstack-from-scratch',
        'paragraph_hash': 1242897,
        'comment_hash': 1242837,
        'deleted': False,
        'text': "Is he in Jersey?",
        'commenter': commenter
    }
    Comment.objects.create(**new_comment_data)
    old_comment_data = {
        'article_url': 'http://0.0.0.0:8080/saltstack-from-scratch',
        'paragraph_hash': 1242897,
        'comment_hash': 2428378341,
        'deleted': False,
        'text': "Heed not the rebel who screams revolution",
        'commenter': commenter,
    }
    old_comment = Comment.objects.create(**old_comment_data)
    old_comment.timestamp = datetime.today() - timedelta(minutes=20)
    old_comment.save()


    call_command('send_mail', '15')

    assert 1 == len(mail.outbox)
    assert new_comment_data['text'] in mail.outbox[0].body
    assert old_comment_data['text'] not in mail.outbox[0].body

@pytest.mark.django_db
def test_email_no_comments():
    test_token = 'fjkdls0u4089riopjwirf'
    commenter_data = {
        'login': 'amfarrell',
        'email': 'amfarrell@mit.edu',
        'name': 'Andrew M. Farrell',
        'avatar_url': "https://avatars.githubusercontent.com/u/123831?v=3",
        'token': test_token,
    }
    commenter = Commenter.objects.create(**commenter_data)
    old_comment_data = {
        'article_url': 'http://0.0.0.0:8080/saltstack-from-scratch',
        'paragraph_hash': 1242897,
        'comment_hash': 2428378341,
        'deleted': False,
        'text': "You say... the price of my war's not a price that you're willing to pay",
        'commenter': commenter,
    }
    old_comment = Comment.objects.create(**old_comment_data)
    old_comment.timestamp = datetime.today() - timedelta(minutes=20)
    old_comment.save()

    call_command('send_mail', '15')

    assert 0 == len(mail.outbox)
