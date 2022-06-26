# Generated by Django 3.2.10 on 2022-05-22 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_data', '0010_auto_20220126_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='semester_name',
            field=models.CharField(choices=[('SEMESTER I', 'SEMESTER I'), ('SEMESTER II', 'SEMESTER II'), ('TRIMESTER I', 'TRIMESTER I'), ('TRIMESTER II', 'TRIMESTER II'), ('TRIMESTER III', 'TRIMESTER III'), ('SUMMER TERM', 'SUMMER TERM')], default='TRIMESTER I', max_length=100, verbose_name='Term Name'),
        ),
    ]
