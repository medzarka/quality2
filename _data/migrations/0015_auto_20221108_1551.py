# Generated by Django 3.2.13 on 2022-11-08 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('_data', '0014_alter_course_cfi_cfi_version_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='upgrade',
            fields=[
                ('upgrade_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Upgrade ID')),
                ('original_filename_path', models.CharField(default='', max_length=250, verbose_name='Original Filename Path')),
                ('temporary_filename_path', models.CharField(default='', max_length=250, verbose_name='Temporary Filename Path')),
                ('temporary_filename', models.CharField(default='', max_length=250, verbose_name='Temporary Filename')),
                ('status', models.CharField(choices=[('I', 'Record Created'), ('T', 'TemporaryFile named'), ('C', 'Original Copied to the temporary file'), ('U', 'The file field is upgraded.'), ('F', 'Finished'), ('E', 'Error occurred')], default='I', max_length=1)),
                ('description', models.CharField(max_length=250, verbose_name='Progress Description')),
            ],
            options={
                'verbose_name': 'Upgrade',
                'verbose_name_plural': 'Upgrades',
                'ordering': ['status'],
            },
        ),
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(max_length=255, verbose_name='Course Name'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_name_ar',
            field=models.CharField(max_length=255, verbose_name='Course Arabic Name'),
        ),
        migrations.AlterField(
            model_name='email',
            name='email_sender',
            field=models.CharField(default='tanomah.quality', max_length=250, verbose_name='Email Sender'),
        ),
        migrations.AlterField(
            model_name='link',
            name='link_description',
            field=models.CharField(max_length=255, unique=True, verbose_name='Link Description'),
        ),
        migrations.AlterField(
            model_name='link',
            name='link_url',
            field=models.CharField(max_length=255, unique=True, verbose_name='Link URL'),
        ),
        migrations.AlterField(
            model_name='program',
            name='program_name',
            field=models.CharField(max_length=255, verbose_name='Program Name'),
        ),
        migrations.AlterField(
            model_name='program',
            name='program_name_ar',
            field=models.CharField(max_length=255, verbose_name='Program Arabic Name'),
        ),
        migrations.AlterField(
            model_name='program',
            name='program_version',
            field=models.CharField(max_length=255, verbose_name='Program Version'),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='specialization_name',
            field=models.CharField(max_length=255, verbose_name='Program Name'),
        ),
        migrations.AlterField(
            model_name='specialization',
            name='specialization_name_ar',
            field=models.CharField(max_length=255, verbose_name='Program Arabic Name'),
        ),
        migrations.AddIndex(
            model_name='upgrade',
            index=models.Index(fields=['original_filename_path'], name='Ddata_upgra_origina_fb4b4f_idx'),
        ),
        migrations.AddIndex(
            model_name='upgrade',
            index=models.Index(fields=['status'], name='Ddata_upgra_status_750cee_idx'),
        ),
    ]
