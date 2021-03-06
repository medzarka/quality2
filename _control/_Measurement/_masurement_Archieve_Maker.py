import threading
import time
import logging
import shutil
import os
from _data._data_measurement import GradesFile, CourseFile, DepartmentFile, MeasurementExportFile
from django.core.files import File

from random import randint
from datetime import datetime


class MeasurementArchiveMakerThread(threading.Thread):
    def __init__(self, semester, teacher):
        threading.Thread.__init__(self)
        self._selected_semester = semester
        self._teacher = teacher
        self.logger = logging.getLogger('db')

    def make_archive(self, source, destination):
        base_name = '.'.join(destination.split('.')[:-1])
        format = destination.split('.')[-1]
        root_dir = os.path.dirname(source)
        base_dir = os.path.basename(source.strip(os.sep))
        shutil.make_archive(base_name, format, root_dir, base_dir)

    def createDir(self, path):
        try:
            os.makedirs(path)
        except FileExistsError as e:
            print(e)
        except FileNotFoundError as ee:
            print(ee)

    def run(self):
        start_time = datetime.now()
        try:
            self.logger.debug(
                f'Start creating the archive file for the semester {self._selected_semester} by the faculty {self._teacher} ')
            year_txt = self._selected_semester.semester_academic_year.academic_year_name.replace('-', '_')
            term_txt = self._selected_semester.semester_name.replace(' ', '')

            _export = MeasurementExportFile()
            _export.semester = self._selected_semester
            _export.teacher = self._teacher
            _export.save()

            filename = f'Measurement_Reports_{year_txt}_{term_txt}_{_export.submission_time}'
            _basedir = os.path.join('/', 'tmp', 'uKKU', filename)
            _sections_dir = os.path.join(_basedir, 'sections')
            _courses_dir = os.path.join(_basedir, 'courses')
            _departments_dir = os.path.join(_basedir, 'departments')

            self.createDir(_basedir)
            self.createDir(_sections_dir)
            self.createDir(_courses_dir)
            self.createDir(_departments_dir)
            self.logger.debug(f'creating the tmp directory in {_basedir}')

            self.logger.debug(f'[1] - Working with the Section Reports.')

            for _report in GradesFile.objects.filter(semester=self._selected_semester):
                try:
                    _tmp_dir = os.path.join(_basedir, 'sections', f'{_report.campus_name}')
                    self.createDir(_tmp_dir)
                    dst = os.path.join(_tmp_dir,
                                       f'section_{_report.section_code}__({_report.section_courseObj.course_code}__{_report.section_courseObj.course_name}).doc')
                    shutil.copyfile(_report.report_file.path, dst)
                    self.logger.debug(f'making section report to {dst}')
                except ValueError as e:
                    self.logger.exception(e)
                    self.logger.error(f'error for making section report to {dst}')


            self.logger.debug(f'[2] - Working with the Course Reports.')
            for _report in CourseFile.objects.filter(semester=self._selected_semester):
                try:
                    dst = os.path.join(_courses_dir, f'course_{_report.course_name}.doc')
                    shutil.copyfile(_report.report_file.path, dst)
                    self.logger.debug(f'making course report to {dst}')
                except ValueError as e:
                    self.logger.exception(e)
                    self.logger.error(f'error for making course report to {dst}')


            self.logger.debug(f'[3] - Working with the Department Reports.')
            for _report in DepartmentFile.objects.filter(semester=self._selected_semester):
                try:
                    dst = os.path.join(_departments_dir, f'department_{_report.department.department_name}.doc')
                    shutil.copyfile(_report.report_file.path, dst)
                    self.logger.debug(f'making department report to {dst}')
                except ValueError as e:
                    self.logger.exception(e)
                    self.logger.error(f'error for making department report to {dst}')


            self.logger.debug(f'[4] - Working with the Zip file.')
            source = _basedir
            destination = _basedir + '.zip'
            self.make_archive(source, destination)
            shutil.rmtree(_basedir)
            end_time = datetime.now()

            _export.export_file.save(filename, File(open(destination, 'rb')))
            _export.elapsedTime = '{}'.format(end_time - start_time)
            _export.state = 1
            _export.save()
            self.logger.debug(f'[5] - Archive created.')

        except Exception as e:
            self.logger.exception(e)
            self.logger.error(f'Error in creating the archive file !')
            end_time = datetime.now()
            _export.state = -1
            _export.elapsedTime = '{}'.format(end_time - start_time)
            _export.save()
