# Generated by Django 4.1.10 on 2023-07-13 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcases',
            name='questionId',
            field=models.IntegerField(max_length=100, null=True),
        ),
    ]
