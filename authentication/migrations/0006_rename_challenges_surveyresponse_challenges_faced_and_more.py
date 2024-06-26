# Generated by Django 5.0.6 on 2024-06-19 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_surveyresponse'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveyresponse',
            old_name='challenges',
            new_name='challenges_faced',
        ),
        migrations.RenameField(
            model_name='surveyresponse',
            old_name='website_changes',
            new_name='changes_request',
        ),
        migrations.RemoveField(
            model_name='surveyresponse',
            name='submitted_at',
        ),
        migrations.AlterField(
            model_name='surveyresponse',
            name='assessment_quality',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='surveyresponse',
            name='overall_experience',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='surveyresponse',
            name='satisfaction',
            field=models.IntegerField(),
        ),
    ]
