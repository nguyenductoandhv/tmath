# Generated by Django 2.2.28 on 2022-07-25 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0147_auto_20220710_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='testcase_visibility_mode',
            field=models.CharField(choices=[('O', 'Visible for authors'), ('C', 'Visible if user is not in a contest'), ('A', 'Always visible')], default='O', max_length=1, verbose_name='Testcase visibility'),
        ),
    ]
