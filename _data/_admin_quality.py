from django.contrib import admin
from django.conf import settings
from django.core.files import File

import uuid
import os
import logging



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
            # update the original paths
            _fields[_field].append(_field.path)
            logger.debug(f'\tworking with the file {_field.path}')
            # update the new temporary paths
            _fields[_field].append(f'{str(uuid.uuid4())}.{_field.path.split(".")[-1]}')

            # copy the files
            _destination_filename = os.path.join(_destination_dir, _fields[_field][1])
            logger.debug(f'\tthe destination file is  {_destination_filename}')
            os.system(f'cp {_fields[_field][0]} {_destination_filename}')
            logger.debug(f'\tthe copy is script is :: "cp {_fields[_field][0]} {_destination_filename}"')
            logger.debug(f'\tthe copy is done from  {_field.path} to {_destination_filename}')

            # update the field
            _field.save(os.path.basename(_destination_filename), File(open(_destination_filename, "wb")), save=True)
            logger.debug(f'\tthe field is updated')

            os.remove(_fields[_field][0])
            logger.debug(f'\tthe file {_fields[_field][0]} is deleted')
            os.remove(_destination_filename)
            logger.debug(f'\tthe file {_destination_filename} is deleted')

        except:
            pass

    cfi_obj.save()
    logger.debug(f'The course file index with id {cfi_obj.course_cfi_id} is updated.')


class Course_CFIAdmin(admin.ModelAdmin):
    list_display = (
        'course_cfi_id', 'campus', 'courseFullName', 'department', 'section',
        'teacher', 'semester')
    list_filter = ('gradeFile__semester', )
    search_fields = ('gradeFile__section_code',)

    #os.system('cp source.txt destination.txt')
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
