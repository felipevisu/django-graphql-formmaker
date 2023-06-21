import graphene
from graphene_django import DjangoConnectionField

from .mutations import CreateResponse
from .types import Survey


class Query(graphene.ObjectType):
    survey = graphene.relay.Node.Field(Survey)
    surveys = DjangoConnectionField(Survey)


class Mutation(graphene.ObjectType):
    create_response = CreateResponse.Field()
