import graphene
from graphene_django.debug import DjangoDebug

from .survey.schema import Mutation as SurveyMutation
from .survey.schema import Query as SurveyQuery


class Query(SurveyQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(SurveyMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
