# Generated by Django 4.2.2 on 2023-06-29 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0006_question_order_questionvalue_order"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="question",
            options={"ordering": ["order"]},
        ),
        migrations.AlterModelOptions(
            name="questionvalue",
            options={"ordering": ["order"]},
        ),
    ]
