import graphene
from graphene import relay
from graphene_django import DjangoConnectionField, DjangoObjectType

from ...survey import models
from .dataloaders import QuestionsByEntryIdLoader


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


class Survey(DjangoObjectType):
    questions = DjangoConnectionField(Question)

    class Meta:
        model = models.Survey
        interfaces = (relay.Node,)

    @staticmethod
    def resolve_questions(root, info, **kargs):
        return QuestionsByEntryIdLoader(info.context).load(root.id)
