# Generated by Django 3.0.7 on 2020-06-28 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_module', '0005_auto_20200628_0647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='daily',
            name='covid_test',
        ),
        migrations.RemoveField(
            model_name='daily',
            name='covid_test_outcome',
        ),
        migrations.AddField(
            model_name='user',
            name='covid_test',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='covid_test_outcome',
            field=models.BooleanField(default=False),
        ),
    ]