from django.db import models
from django.conf import settings

import uuid
import shutil
import os


class upgrade(models.Model):
    PROGRESS = (
        ('I', 'Record Created'),
        ('T', 'TemporaryFile named'),
        ('C', 'Original Copied to the temporary file'),
        ('U', 'The file field is upgraded.'),
        ('E', 'Error occurred'),
    )

    upgrade_id = models.BigAutoField(primary_key=True, verbose_name='Upgrade ID')
    original_filename_path = models.CharField(max_length=1024, verbose_name='Original Filename', default=None)
    temporary_filename_path = models.CharField(max_length=1024, verbose_name='Temporary Filename', default=None)
    status = models.CharField(max_length=1, choices=PROGRESS, default= 'I')
    description = models.CharField(max_length=1024, verbose_name='Progress Description')

    def do_createTemporary_filename(self):
        if self.original_filename_path is not None and self.original_filename_path != '':
            tmp_filename = f'{str(uuid.uuid4())}.{self.original_filename_path.split(".")[-1]}'
            self.temporary_filename_path = os.path.join(settings.SITE_TMP_DIR, tmp_filename)
            self.status = 'T'
        else:
            self.status = 'E'
            self.description = self.description + '\nUnable to create temporary file because the original file is not correctly set.'
        self.save()

    def do_copy(self, mode='python'):
        try:
            cp_source = self.original_filename_path
            cp_destination = self.temporary_filename_path
            cp_source_obj = open(cp_source, 'rb')
            cp_destination_obj = open(cp_destination, 'wb')

            if mode == 'python':
                shutil.copyfileobj(cp_source_obj, cp_destination_obj)
            else:
                os.system(f'cp {cp_source} {cp_destination}')
            self.status = 'C'

        except Exception as e:
            self.status = 'E'
            self.description = self.description + '\nUnable to copy the original file.'
            self.description = self.description + f'\nThe error is {str(e)}'

        self.save()


    def do_upgrade(self, data_filefield):
        '''
        if self.status == 'C':
        f = open(self.temporary_filename_path, mode='rb')
        _field.save(temporary_filename, File(f), save=True)
        logger.debug(f'\tthe field is updated')

        os.remove(original_path)
        logger.debug(f'\tthe file {original_filename} is deleted')
        os.remove(temporary_path)
        logger.debug(f'\tthe file {temporary_path} is deleted')
        '''
        pass


    class Meta:
        ordering = ['status']
        verbose_name_plural = 'Upgrades'
        verbose_name = 'Upgrade'
        indexes = [
            models.Index(fields=['original_filename_path', ]),
            models.Index(fields=['status', ]),
        ]