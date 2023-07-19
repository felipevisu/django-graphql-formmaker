from collections import defaultdict

from ...survey.models import Question
from ..core.dataloaders import DataLoader


class QuestionsByEntryIdLoader(DataLoader):
    context_key = "questions_by_survey_id"

    def batch_load(self, keys):
        questions_by_survey_ids = defaultdict(list)
        for question in Question.objects.filter(survey_id__in=keys).iterator():
            questions_by_survey_ids[question.survey_id].append(question)
        return [questions_by_survey_ids.get(key, []) for key in keys]
