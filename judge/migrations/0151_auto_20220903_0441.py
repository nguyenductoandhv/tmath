# Generated by Django 2.2.28 on 2022-09-03 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0150_profile_typo_contest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='organizations',
            field=models.ManyToManyField(blank=True, related_name='members', related_query_name='member', to='judge.Organization', verbose_name='organization'),
        ),
    ]