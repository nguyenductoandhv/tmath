# Generated by Django 4.1.9 on 2023-06-17 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0170_alter_contest_authors_alter_contest_curators_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_totp_enabled',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_totp_timecode',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='scratch_codes',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='totp_key',
        ),
        migrations.AddField(
            model_name='profile',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
