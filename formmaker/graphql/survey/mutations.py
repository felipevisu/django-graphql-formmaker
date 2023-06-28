import graphene
from graphql_relay import from_global_id

from ...response import models as response_models
from ...survey import models as survey_models
from ..core.mutations import BaseMutation
from .mixins import CleanSurveyMixin
from .types import Survey


class AnswerInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    values = graphene.List(graphene.String)


class ResponseInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    answers = graphene.List(AnswerInput)


class CreateResponse(CleanSurveyMixin, BaseMutation):
    class Arguments:
        input = ResponseInput(required=True)

    survey = graphene.Field(Survey)

    @classmethod
    def save(cls, input):
        global_id = input.get("id")
        id = from_global_id(global_id).id
        response = response_models.Response.objects.create(survey_id=id)
        answers = input.get("answers")
        for question_answer in answers:
            id = from_global_id(question_answer["id"]).id
            question = survey_models.Question.objects.filter(id=id).first()
            answer = response_models.Answer.objects.create(
                question=question,
                response=response,
                question_body=question.name,
            )
            values = question_answer.get("values")
            for value in values:
                response_models.Value.objects.create(value=value, answer=answer)

    @classmethod
    def perform_mutation(cls, root, info, input):
        survey = cls.clean_input(input)
        cls.save(input)
        return CreateResponse(survey=survey)
