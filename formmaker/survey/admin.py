from django.contrib import admin

from .models import Question, Survey


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Survey)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "updated"]
    inlines = [QuestionInline]
