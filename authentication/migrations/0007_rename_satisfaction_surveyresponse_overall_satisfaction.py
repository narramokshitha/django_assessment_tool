# Generated by Django 5.0.6 on 2024-06-19 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_rename_challenges_surveyresponse_challenges_faced_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveyresponse',
            old_name='satisfaction',
            new_name='overall_satisfaction',
        ),
    ]
