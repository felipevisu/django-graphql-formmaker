import graphene
from graphene_django import DjangoConnectionField

from .types import Survey


class Query(graphene.ObjectType):
    survey = graphene.relay.Node.Field(Survey)
    surveys = DjangoConnectionField(Survey)
