# Generated by Django 3.2.16 on 2022-11-13 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0159_alter_problem_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='problemtype',
            name='priority',
            field=models.BooleanField(default=False, verbose_name='priority'),
        ),
    ]
