# Generated by Django 4.1.9 on 2024-06-19 03:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0179_contest_fastio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='memory_limit',
            field=models.PositiveIntegerField(default=256000, help_text='The memory limit for this problem, in kilobytes (e.g. 64mb = 65536 kilobytes).', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1048576)], verbose_name='memory limit'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='points',
            field=models.FloatField(default=100, help_text="Points awarded for problem completion. Points are displayed with a 'p' suffix if partial.", validators=[django.core.validators.MinValueValidator(0)], verbose_name='points'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='submission_source_visibility_mode',
            field=models.CharField(choices=[('F', 'Follow global setting'), ('A', 'Always visible'), ('S', 'Visible if problem solved'), ('O', 'Only own submissions')], default='O', max_length=1, verbose_name='submission source visibility'),
        ),
        migrations.AlterField(
            model_name='problem',
            name='time_limit',
            field=models.FloatField(default=1.0, help_text='The time limit for this problem, in seconds. Fractional seconds (e.g. 1.5) are supported.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)], verbose_name='time limit'),
        ),
    ]
