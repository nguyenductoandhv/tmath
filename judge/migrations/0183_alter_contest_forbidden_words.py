# Generated by Django 4.1.9 on 2024-07-17 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0182_contest_forbidden_words'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='forbidden_words',
            field=models.TextField(blank=True, help_text='Words that are forbidden in the source code.', verbose_name='forbidden words'),
        ),
    ]
