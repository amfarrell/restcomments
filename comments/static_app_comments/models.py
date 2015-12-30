from django.db import models

# Create your models here.
class Comment(models.Model):
    article_slug = models.SlugField(max_length=100, db_index=True)
    user_email = models.EmailField()
    paragraph_hash = models.IntegerField(db_index=True)
    timestamp = models.DateTimeField(auto_now = True)
    deleted = models.BooleanField(default=False)
    text = models.TextField()

    class Meta:
        ordering = ('article_slug', 'paragraph_hash', 'timestamp',)
