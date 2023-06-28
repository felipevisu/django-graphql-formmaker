from django.core.exceptions import ValidationError
from graphql_relay import from_global_id

from ...survey import QuestionType
from ...survey import models as survey_models


class CleanSurveyMixin:
    @classmethod
    def clean_values(cls, answer, question, global_id):
        values = answer["values"]
        if question.type != QuestionType.PLAIN_TEXT:
            for value in values:
                question_value = question.values.filter(name=value).first()
                if not question_value:
                    raise ValidationError(
                        {
                            global_id: ValidationError(
                                "This value is not valid for this question"
                            )
                        }
                    )

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
            cls.clean_values(answer, question, global_id)

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
        survey = cls.clean_survey(input)
        cls.clean_questions(input, survey)
        return survey
        return survey
