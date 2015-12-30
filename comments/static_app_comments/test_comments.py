from django.test import TestCase
import py.test

# Create your tests here.

from rest_framework.test import APIRequestFactory

def test_save_comment():
    factory = APIRequestFactory()
    assert 0
    request = factory.post('/comments/', {
        'article_slug': 'saltstack-from-scratch',
        'user_email': 'af@jambonsw.com',
        'paragraph_hash': 1242897,
        'deleted': False,
        'text': "I see a little siluetto of a man.",
    }, format='json')
