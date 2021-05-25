from django.contrib import admin

from .models import Response, Answer

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['pk', 'creation_date', 'finalized', 'session']
    inlines = [AnswerInline]


admin.site.register(Response, ResponseAdmin)