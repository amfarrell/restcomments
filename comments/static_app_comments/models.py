from django.db import models

# Create your models here.
class Comment(models.Model):
    article_url = models.URLField(db_index=True)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=128)
    user_avatar_url = models.URLField()
    paragraph_hash = models.IntegerField(db_index=True)
    comment_hash = models.IntegerField()
    timestamp = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)
    text = models.TextField()

    class Meta:
        ordering = ('article_url', 'paragraph_hash', 'timestamp',)
