from django.db import models

from . import QuestionType


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="nome")
    slug = models.SlugField(max_length=255, verbose_name="atalho")
    description = models.TextField(blank=True, verbose_name="descrição")
    text_1 = models.TextField(blank=True, verbose_name="Média >= 5")
    text_2 = models.TextField(blank=True, verbose_name="2.5 < Média > 5")
    text_3 = models.TextField(blank=True, verbose_name="Média <= 25")

    class Meta:
        ordering = ['pk']
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255, verbose_name="nome")
    description = models.TextField(blank=True, verbose_name="descrição")
    order = models.PositiveIntegerField(default=1, verbose_name="ordem")

    class Meta:
        ordering = ['order']
        verbose_name = "Grupo de perguntas"
        verbose_name_plural = "Grupos de perguntas"

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.TextField(max_length=255, verbose_name="Pergunta")
    number = models.PositiveIntegerField(default=1, verbose_name="número")
    type = models.CharField(max_length=30, choices=QuestionType.CHOICES, default=QuestionType.RANK, verbose_name="tipo")
    options = models.TextField(blank=True, verbose_name="opções")
    category = models.ForeignKey(Category, related_name="questions", verbose_name="categoria", on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, related_name="questions", verbose_name="grupo", on_delete=models.SET_NULL, null=True, blank=True)
    required = models.BooleanField(default=True, verbose_name="obrigatória")

    class Meta:
        ordering = ['number']
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return str(self.number)

    def get_choices(self):
        choices = self.options.split(';')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c,c))
        choices_tuple = tuple(choices_list)
        return choices_tuple