# Generated by Django 3.0 on 2019-12-13 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_web', '0002_auto_20191213_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu_box_item',
            name='menu_box_link',
            field=models.CharField(default='', max_length=250, verbose_name='Item link'),
        ),
    ]