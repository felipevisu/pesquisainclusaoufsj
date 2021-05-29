from django.db import models
from django.contrib.sessions.models import Session

from ..questions.models import Question

class Response(models.Model):
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, verbose_name="sessão", blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="data de criação")
    modification_date = models.DateTimeField(auto_now=True, verbose_name="data de modificação")
    finalized = models.BooleanField(default=False, verbose_name="finalizado")

    class Meta:
        ordering = ['-creation_date']
        verbose_name = "Questionário respondido"
        verbose_name_plural = "Questionários respondidos"


class Answer(models.Model):
    response = models.ForeignKey(Response, related_name='answers', on_delete=models.CASCADE, verbose_name="questionário")
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name="pergunta")
    body = models.CharField(max_length=200, blank=True, null=True, verbose_name="resposta")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="data de criação")
    modification_date = models.DateTimeField(auto_now=True, verbose_name="data de modificação")

    class Meta:
        unique_together = ['response', 'question']
        ordering = ['response', 'question']
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"

    def __str__(self):
        return "Pergunta {}".format(self.question.number)

