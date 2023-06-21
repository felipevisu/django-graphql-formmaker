import graphene

from .types import Survey


class AnswerInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    body = graphene.String(required=True)


class ResponseInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    answers = graphene.List(AnswerInput)


class CreateResponse(graphene.Mutation):
    class Arguments:
        input = ResponseInput(required=True)

    survey = graphene.Field(Survey)

    @classmethod
    def mutate(cls, root, info, input):
        print(input)
        return CreateResponse(survey=None)
