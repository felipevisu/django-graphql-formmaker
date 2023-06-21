from django.contrib import admin

from .models import Answer, Response


class AnswerInline(admin.TabularInline):
    model = Answer


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ["survey", "created"]
    inlines = [AnswerInline]
