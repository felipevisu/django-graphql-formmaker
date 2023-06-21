import graphene
from graphene_django.debug import DjangoDebug

from .survey.schema import Query as SurveyQuery


class Query(SurveyQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query)
