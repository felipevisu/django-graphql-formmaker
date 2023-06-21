# Generated by Django 4.2.2 on 2023-06-21 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0002_survey_created_survey_description_survey_updated_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="survey",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="survey.survey",
            ),
        ),
    ]