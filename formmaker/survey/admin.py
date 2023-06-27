from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import Question, Survey, Value


class ValueInline(NestedStackedInline):
    model = Value
    extra = 1
    fk_name = "question"


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    fk_name = "survey"
    inlines = [ValueInline]


@admin.register(Survey)
class SurveyAdmin(NestedModelAdmin):
    list_display = ["name", "created", "updated"]
    inlines = [QuestionInline]
