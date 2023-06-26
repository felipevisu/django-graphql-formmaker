import graphene
from django.core.exceptions import ValidationError
from graphql_relay import from_global_id

from ...response import models as response_models
from ...survey import models as survey_models
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
    def clean_questions(cls, input, survey):
        answers = input.get("answers")
        for answer in answers:
            global_id = answer["id"]
            id = from_global_id(global_id).id
            if not id:
                raise ValidationError({global_id: ValidationError("Not found")})
            question = survey_models.Question.objects.filter(id=id).first()
            if not question:
                raise ValidationError({global_id: ValidationError("Not found")})
            if question.survey != survey:
                raise ValidationError(
                    {global_id: ValidationError("Question and survey are incompatible")}
                )

    @classmethod
    def clean_survey(cls, input):
        global_id = input.get("id")
        id = from_global_id(global_id).id
        if not id:
            raise ValidationError({global_id: ValidationError("Not found")})
        survey = survey_models.Survey.objects.filter(id=id).first()
        if not survey:
            raise ValidationError({global_id: ValidationError("Not found")})
        return survey

    @classmethod
    def clean_input(cls, input):
        survey = cls.clean_survey(input)
        cls.clean_questions(input, survey)
        return survey

    @classmethod
    def save(cls, input):
        global_id = input.get("id")
        id = from_global_id(global_id).id
        response = response_models.Response.objects.create(survey_id=id)
        answers = input.get("answers")
        for answer in answers:
            id = from_global_id(answer["id"]).id
            question = survey_models.Question.objects.filter(id=id).first()
            response_models.Answer.objects.create(
                question=question,
                response=response,
                answer_body=answer["body"],
                question_body=question.name,
            )

    @classmethod
    def perform_mutation(cls, root, info, input):
        survey = cls.clean_input(input)
        cls.save(input)
        return CreateResponse(survey=survey)
