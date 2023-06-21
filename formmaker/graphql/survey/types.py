from graphene import relay
from graphene_django import DjangoObjectType

from ...survey import models


class Survey(DjangoObjectType):
    class Meta:
        model = models.Survey
        interfaces = (relay.Node,)


class Question(DjangoObjectType):
    class Meta:
        model = models.Question
        interfaces = (relay.Node,)
