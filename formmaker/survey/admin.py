from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline

from .models import Question, QuestionValue, Survey


class QuestionValueInline(NestedStackedInline):
    model = QuestionValue
    extra = 0
    sortable_field_name = "order"


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 0
    sortable_field_name = "order"
    inlines = [QuestionValueInline]


@admin.register(Survey)
class SurveyAdmin(NestedModelAdmin):
    list_display = ["name", "created", "updated"]
    inlines = [QuestionInline]
