import graphene
from django.core.exceptions import ValidationError

from ..core.mutations import BaseMutation
from .types import Survey


class AnswerInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    body = graphene.String(required=True)


class ResponseInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    answers = graphene.List(AnswerInput)


class CreateResponse(BaseMutation):
    class Arguments:
        input = ResponseInput(required=True)

    survey = graphene.Field(Survey)

    @classmethod
    def perform_mutation(cls, root, info, input):
        raise ValidationError({"id": ValidationError("not found")})
