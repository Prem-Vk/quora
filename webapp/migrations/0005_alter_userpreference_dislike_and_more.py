# Generated by Django 5.2 on 2025-04-09 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_userpreference_unique_user_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='dislike',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='like',
            field=models.BooleanField(default=False),
        ),
    ]
