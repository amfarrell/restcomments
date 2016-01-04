from django.contrib.auth.models import User, Group
from comments.static_app_comments.models import Comment

from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('article_url', 'user_email', 'user_name', 'user_avatar_url',
            'paragraph_hash', 'comment_hash', 'timestamp', 'deleted', 'text', )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
