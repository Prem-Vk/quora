# Generated by Django 5.2 on 2025-04-09 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_rename_reaction_userpreference_dislike_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userpreference',
            constraint=models.UniqueConstraint(fields=('user', 'answer'), name='unique_user_answer'),
        ),
    ]
