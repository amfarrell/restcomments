from django.core.management.base import BaseCommand, CommandError
from comments.static_app_comments.models import Comment
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from datetime import datetime, timedelta
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Sends the comments written in the last N minutes'

    def add_arguments(self, parser):
        parser.add_argument('mins', nargs='?', default='30', type=int)

    def render_comments_html(self, comments):
        template = Template("""
        {% for comment in comments %}
            {% if comment.commenter.name %}
            from <a href="https://github.com/{{ comment.commenter.login }}">
                {{ comment.commenter.name }}
            </a>
            {% else %}
            from <a href="https://github.com/{{ comment.commenter.login }}">
                {{ comment.commenter.login }}
            </a>
            {% endif %}
            on <a href="{{ comment.article_url }}">{{ comment.article_url }}</a>:
            {{ comment.text }}
            {% if comment.commenter.email %}
                respond to {{ comment.commenter.email }}
            {% endif %}
        {% endfor %}
        """)
        context = Context({'comments': comments})
        return template.render(context)


    def render_comments_plaintext(self, comments):
        template = Template("""
        {% for comment in comments %}
            {% if comment.commenter.name %}
            from {{ comment.commenter.name }}
            {% else %}
            from {{ comment.commenter.login }}
            {% endif %}
            on {{ comment.article_url }},:
            {{ comment.text }}
        {% endfor %}
        """)
        context = Context({'comments': comments})
        return template.render(context)

    def handle(self, *args, **options):
        comments = Comment.objects.filter(timestamp__gt=
            datetime.today()-timedelta(minutes=options['mins'])).select_related('commenter')
        if comments.count():
            mail = EmailMultiAlternatives(
                subject="Comments on {}".format(settings.ALLOWED_HOSTS),
                body=self.render_comments_plaintext(comments),
                from_email=os.environ.get('SERVER_EMAIL', 'comments@amfarrell.com'),
                to=[os.environ.get('ADMIN_EMAIL', 'amfarrell@mit.edu')],
                headers={'Reply-To': os.environ.get('ADMIN_EMAIL', 'amfarrell@mit.edu')}
            )
            mail.attach_alternative(self.render_comments_html(comments), 'text/html')
            mail.send()
