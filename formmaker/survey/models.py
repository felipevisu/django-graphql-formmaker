from django.db import models

from . import QuestionType


class Survey(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="questions"
    )
    name = models.CharField(max_length=256)
    type = models.CharField(
        max_length=256, choices=QuestionType.choices, default=QuestionType.PLAIN_TEXT
    )

    def __str__(self):
        return self.name


class QuestionValue(models.Model):
    name = models.CharField(max_length=256)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="values"
    )

    def __str__(self):
        return self.name
