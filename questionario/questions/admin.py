from django.contrib import admin

from .models import Category, Group, Question

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class GroupAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["number", "question", "group", "type"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Group, GroupAdmin)    
admin.site.register(Question, QuestionAdmin)