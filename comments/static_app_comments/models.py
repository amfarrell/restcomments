from django.db import models
from rest_framework.authtoken.models import Token

class Commenter(models.Model):
    login = models.CharField(primary_key=True, max_length=48)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=128, null=True)
    avatar_url = models.URLField(null=True)
    banned = models.BooleanField(default=False)
    token = models.CharField(max_length=40)


# Create your models here.
class Comment(models.Model):
    commenter = models.ForeignKey(Commenter)
    article_url = models.URLField(db_index=True)
    paragraph_hash = models.BigIntegerField(db_index=True)
    comment_hash = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)
    text = models.TextField()

    class Meta:
        ordering = ('article_url', 'paragraph_hash', 'timestamp',)
