from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
