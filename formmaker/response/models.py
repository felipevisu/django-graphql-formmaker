from django.db import models

from ..survey.models import Question, Survey


class Response(models.Model):
    survey = models.ForeignKey(
        Survey,
        related_name="responses",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    response = models.ForeignKey(
        Response, related_name="answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, on_delete=models.SET_NULL, null=True, blank=True
    )
    question_body = models.TextField()


class Value(models.Model):
    value = models.CharField(max_length=256)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="values")
