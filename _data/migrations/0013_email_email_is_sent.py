# Generated by Django 3.2.10 on 2022-05-28 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_data', '0012_auto_20220528_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='email_is_sent',
            field=models.BooleanField(default=False, verbose_name='Email Sent ?'),
        ),
    ]