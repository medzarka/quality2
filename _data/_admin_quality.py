from django.contrib import admin
from django.conf import settings
from django.core.files import File

import uuid
import os
import logging
import shutil

from _data._data_quality import Course_CFI, ReviewerAffectations, QualityExportFile


def update_file_field(cfi_obj, logger):
    logger.debug(f'############################################################')
    logger.debug(f'Working with the course file index with id {cfi_obj.course_cfi_id}')
    _fields = {}
    _fields[cfi_obj.course_specification_file] = []
    _fields[cfi_obj.exams_samples_file] = []
    _fields[cfi_obj.marks_file] = []
    _fields[cfi_obj.clos_measurement_file] = []
    _fields[cfi_obj.course_report_file] = []
    _fields[cfi_obj.kpis_measurements_file] = []
    _fields[cfi_obj.instructor_schedule_file] = []
    _fields[cfi_obj.course_plan_file] = []
    _fields[cfi_obj.curriculum_vitae_file] = []
    _fields[cfi_obj.report_cfi] = []
    _fields[cfi_obj.report_cfr] = []
    logger.debug(f'Dictionary created for course file index with id {cfi_obj.course_cfi_id}')

    _destination_dir = os.path.join(settings.SITE_TMP_DIR, 'uKKU2', 'tmp')
    os.makedirs(_destination_dir, exist_ok=True)
    logger.debug(f'Temporary directory is created : {_destination_dir}')

    for _field in _fields.keys():
        try:
            logger.debug(f'------------------------------')
            original_filename = os.path.basename(_field.path)
            original_path = _field.path
            temporary_filename = f'{str(uuid.uuid4())}.{_field.path.split(".")[-1]}'
            temporary_path = os.path.join(_destination_dir, temporary_filename)

            # update the original paths
            _fields[_field].append(original_path)
            logger.debug(f'\tworking with the file {original_path}')
            # update the new temporary paths
            _fields[_field].append(temporary_path)
            logger.debug(f'\tthe temporary filename is  {temporary_path}')

            # copy the files

            cp_source = original_path#.replace(" ", "\ ")
            import codecs
            cp_source_obj = codecs.open(cp_source, 'rb')
            cp_destination = temporary_path#.replace(" ", "\ ")
            cp_destination_obj = codecs.open(cp_destination, 'wb')
            #logger.debug(f'\tthe copy is script is :: "cp {cp_source} {cp_destination}"')
            #os.system(f'cp {cp_source} {cp_destination}')
            shutil.copyfileobj(cp_source_obj, cp_destination_obj)
            logger.debug(f'\tthe copy is done from  {original_filename} to {temporary_filename}')

            # update the field

            f = open(temporary_path, mode='rb')
            _field.save(temporary_filename, File(f), save=True)
            logger.debug(f'\tthe field is updated')

            os.remove(original_path)
            logger.debug(f'\tthe file {original_filename} is deleted')
            os.remove(temporary_path)
            logger.debug(f'\tthe file {temporary_path} is deleted')

        except Exception as e:
            logger.exception(e)

    cfi_obj.save()
    logger.debug(f'The course file index with id {cfi_obj.course_cfi_id} is updated.')


class Course_CFIAdmin(admin.ModelAdmin):
    list_display = (
        'course_cfi_id', 'campus', 'courseFullName', 'department', 'section',
        'teacher', 'semester')
    list_filter = ('gradeFile__semester',)
    search_fields = ('gradeFile__section_code',)

    # os.system('cp source.txt destination.txt')
    def update_paths(modeladmin, request, queryset):
        logger = logging.getLogger('db')
        logger.debug(f'[update_paths_quality] logger initialized.')
        for _cfi_report in queryset:
            if _cfi_report.gradeFile.section_courseObj is None:
                continue
            else:
                update_file_field(_cfi_report, logger=logger)

    update_paths.short_description = 'Apply update paths'
    actions = [update_paths, ]  # <-- Add the list action function here


admin.site.register(Course_CFI, Course_CFIAdmin)


class ReviewerAffectationsAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'reviewer',)
    list_filter = ('semester',)
    # search_fields = ('course_name',)


admin.site.register(ReviewerAffectations, ReviewerAffectationsAdmin)


class QualityExportFileAdmin(admin.ModelAdmin):
    list_display = (
        'quality_export_file_id', 'teacher', 'submission_time', 'state', 'elapsedTime', 'exec_trace', 'export_file')
    list_filter = ('semester', 'state')
    # search_fields = ('course_name',)


admin.site.register(QualityExportFile, QualityExportFileAdmin)
