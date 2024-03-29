# Generated by Django 3.2.10 on 2022-01-16 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('_data', '0007_auto_20211227_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('link_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Link ID')),
                ('link_description', models.CharField(max_length=255, unique=True, verbose_name='Link Description')),
                ('link_url', models.CharField(max_length=255, unique=True, verbose_name='Link URL')),
                ('link_time', models.DateTimeField(auto_now=True, verbose_name='Link Submission time')),
                ('link_semester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='_data.semester')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
                'ordering': ['link_time'],
            },
        ),
        migrations.AddIndex(
            model_name='link',
            index=models.Index(fields=['link_time'], name='Ddata_link_link_ti_a90ac5_idx'),
        ),
        migrations.AddIndex(
            model_name='link',
            index=models.Index(fields=['link_semester'], name='Ddata_link_link_se_18be5e_idx'),
        ),
    ]
