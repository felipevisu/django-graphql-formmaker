import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from ...survey import models


class Survey(DjangoObjectType):
    class Meta:
        model = models.Survey
        interfaces = (relay.Node,)


class QuestionValue(DjangoObjectType):
    class Meta:
        model = models.QuestionValue
        interfaces = (relay.Node,)


class Question(DjangoObjectType):
    values = graphene.List(QuestionValue)

    class Meta:
        model = models.Question
        interfaces = (relay.Node,)

    @staticmethod
    def resolve_values(question, *args, **kwargs):
        return question.values.all()
