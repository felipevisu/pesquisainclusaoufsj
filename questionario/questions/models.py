from django.db import models

from . import QuestionType


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    text_1 = models.TextField("Média >= 5", blank=True)
    text_2 = models.TextField("2.5 < Média > 5", blank=True)
    text_3 = models.TextField("Média <= 25", blank=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.TextField(max_length=255)
    number = models.PositiveIntegerField(default=1)
    type = models.CharField(max_length=30, choices=QuestionType.CHOICES, default=QuestionType.RANK)
    options = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name="questions", on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, related_name="questions", on_delete=models.SET_NULL, null=True, blank=True)
    required = models.BooleanField(default=True)

    class Meta:
        ordering = ['number']

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