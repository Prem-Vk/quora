# Generated by Django 5.2 on 2025-04-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_alter_answer_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpreference',
            old_name='reaction',
            new_name='dislike',
        ),
        migrations.AddField(
            model_name='userpreference',
            name='like',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
