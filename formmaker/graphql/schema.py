import graphene

from .survey.schema import Query as SurveyQuery


class Query(SurveyQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
