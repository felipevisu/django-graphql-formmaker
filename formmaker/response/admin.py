from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import Answer, Response, Value


class ReadOnlyMixin:
    editable_fields = []
    readonly_fields = []
    exclude = []

    def get_readonly_fields(self, *params):
        return list(self.readonly_fields) + [
            field.name
            for field in self.model._meta.fields
            if field.name not in self.editable_fields and field.name not in self.exclude
        ]

    def has_add_permission(self, *params):
        return False

    def has_delete_permission(self, *params):
        return False


class ValueInline(ReadOnlyMixin, NestedStackedInline):
    model = Value
    extra = 1
    fk_name = "answer"


class AnswerInline(ReadOnlyMixin, NestedStackedInline):
    model = Answer
    extra = 1
    fk_name = "response"
    inlines = [ValueInline]


@admin.register(Response)
class ResponseAdmin(ReadOnlyMixin, NestedModelAdmin):
    list_display = ["survey", "created"]
    inlines = [AnswerInline]
