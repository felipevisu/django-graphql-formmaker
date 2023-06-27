from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import Question, QuestionValue, Survey


class QuestionValueInline(NestedStackedInline):
    model = QuestionValue
    extra = 1
    fk_name = "question"


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    fk_name = "survey"
    inlines = [QuestionValueInline]


@admin.register(Survey)
class SurveyAdmin(NestedModelAdmin):
    list_display = ["name", "created", "updated"]
    inlines = [QuestionInline]
