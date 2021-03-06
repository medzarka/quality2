# Generated by Django 3.2.10 on 2022-01-26 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_data', '0008_auto_20220116_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='departmentfile',
            name='number_of_courses',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Number of Courses'),
        ),
        migrations.AddField(
            model_name='departmentfile',
            name='stat_anova_sig',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='ANNOVA Sig.'),
        ),
        migrations.AddField(
            model_name='departmentfile',
            name='stat_anova_value',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='ANNOVA value'),
        ),
        migrations.AddField(
            model_name='departmentfile',
            name='stat_eta_sig',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Eta Test Sig.'),
        ),
        migrations.AddField(
            model_name='departmentfile',
            name='stat_eta_value',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Eta Test Value'),
        ),
    ]
