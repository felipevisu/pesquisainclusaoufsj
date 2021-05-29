import csv
from django.http import HttpResponse
from django.contrib import admin

from ..questions.models import Question
from .models import Response, Answer

def get_answers(questions, obj):
    response = []
    answers = obj.answers.all()
    for question in questions:
        answer = answers.filter(question_id=question).first()
        if answer:
            response.append(answer.body)
        else:
            response.append(None)
    return response


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        questions = Question.objects.order_by("number")
        questions_ids = [question.id for question in questions]
        questions_names = ["Questão {}".format(question.number) for question in questions]

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names + questions_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names] + get_answers(questions_ids, obj))

        return response

    export_as_csv.short_description = "Exportar selecionados"


class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


class ResponseAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['pk', 'creation_date', 'finalized']
    list_filter = ['finalized']
    actions = ["export_as_csv"]
    inlines = [AnswerInline]


admin.site.register(Response, ResponseAdmin)