from django.db import models
from django.conf import settings
from django.core.files import File

import uuid
import shutil
import os


class upgrade(models.Model):
    PROGRESS = (
        ('I', 'Record Created'),
        ('T', 'TemporaryFile named'),
        ('C', 'Original Copied to the temporary file'),
        ('U', 'The file field is upgraded.'),
        ('F', 'Finished'),
        ('E', 'Error occurred'),
    )

    upgrade_id = models.BigAutoField(primary_key=True, verbose_name='Upgrade ID')
    original_filename_path = models.CharField(max_length=1024, verbose_name='Original Filename Path', default='')
    temporary_filename_path = models.CharField(max_length=1024, verbose_name='Temporary Filename Path', default='')
    temporary_filename = models.CharField(max_length=1024, verbose_name='Temporary Filename', default='')
    status = models.CharField(max_length=1, choices=PROGRESS, default='I')
    description = models.CharField(max_length=1024, verbose_name='Progress Description')


    def do_createTemporary_filename(self):
        if self.status == 'I':
            if self.original_filename_path is not None and self.original_filename_path != '':
                self.temporary_filename = f'{str(uuid.uuid4())}.{self.original_filename_path.split(".")[-1]}'
                self.temporary_filename_path = os.path.join(settings.SITE_TMP_DIR, self.temporary_filename)
                self.status = 'T'
            else:
                self.status = 'E'
                self.description = self.description + '\n (1) Unable to create temporary file because the original file is not correctly set.'
            self.save()
        else:
            raise Exception('File Upgrade Error (1) :: it looks like that the temporary file is already created.')

    def do_copy(self, mode='python'):
        if self.status == 'T':
            try:
                cp_source = self.original_filename_path
                cp_destination = self.temporary_filename_path
                self.description = self.description + '\n(2) Opening the temporary file.'
                cp_destination_obj = open(cp_destination, 'wb')
                self.description = self.description + '\n(2) Opening the original file.'
                cp_source_obj = open(cp_source, 'rb')
                self.description = self.description + '\n(2) Files are open now.'

                if mode == 'python':
                    shutil.copyfileobj(cp_source_obj, cp_destination_obj)
                else:
                    os.system(f'cp {cp_source} {cp_destination}')
                self.status = 'C'

            except Exception as e:
                self.status = 'E'
                self.description = self.description + '\n(2) Unable to copy the original file.'
                self.description = self.description + f'\n(2) The error is {str(e)}'

            self.save()
        else:
            raise Exception(
                'File Upgrade Error (2) :: it looks like that the temporary file is already copied or that the temporary file is not yet created.')

    def do_upgrade(self, data_filefield):
        if self.status == 'C':
            f = open(self.temporary_filename_path, mode='rb')
            data_filefield.save(self.temporary_filename, File(f), save=True)
            self.status = 'U'

            self.save()

        else:
            raise Exception(
                'File Upgrade Error (3) :: it looks like that the temporary file is already copied, or not yet created.')

    def do_clean(self):
        if self.status == 'U':
            os.remove(self.temporary_filename_path)
            os.remove(self.original_filename_path)
            self.status = 'F'
            self.save()
        else:
            raise Exception(
                'File Upgrade Error (4) :: it looks like that the file upgrade process is already clean or some process are not yet completed.')

    class Meta:
        ordering = ['status']
        verbose_name_plural = 'Upgrades'
        verbose_name = 'Upgrade'
        indexes = [
            models.Index(fields=['original_filename_path', ]),
            models.Index(fields=['status', ]),
        ]
