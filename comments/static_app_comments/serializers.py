from django.contrib.auth.models import User, Group
from comments.static_app_comments.models import Comment, Commenter

from rest_framework import serializers

class CommenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commenter
        fields = ('login', 'email', 'name', 'avatar_url', )

    def to_internal_value(self, data):
        return Commenter.objects.get(login=data['login'])

class CommentSerializer(serializers.ModelSerializer):
    commenter = CommenterSerializer()

    class Meta:
        model = Comment
        fields = ('article_url', 'commenter', 'paragraph_hash',
                  'comment_hash', 'timestamp', 'deleted', 'text', )
        read_only_fields = ('timestamp', 'commenter')

    def create(self, validated_data):
        if 'user' in validated_data:
            validated_data['commenter'] = validated_data.pop('user')
        return Comment.objects.create(**validated_data)
