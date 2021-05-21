from django.db import models
from django.contrib.sessions.models import Session

from ..questions.models import Question

class Response(models.Model):
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    interview_uuid = models.CharField("Identificador", max_length=36)
    creation_date = models.DateTimeField('data de criação', auto_now_add=True)
    modification_date = models.DateTimeField('data de modificação', auto_now=True)
    finalized = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creation_date']


class Answer(models.Model):
    response = models.ForeignKey(Response, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['response', 'question']
        ordering = ['response', 'question']