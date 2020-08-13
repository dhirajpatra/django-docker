from __future__ import absolute_import, unicode_literals
from celery import task
import os
import django
import logging
from datetime import datetime, timedelta
import xlsxwriter
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_task_manager.settings')
django.setup()
from task_manager.models import Task

@task
def weekly_task_report_of_employers():
    logging.info('start')
    last_date = datetime.now() - timedelta(weeks=1)
    tasks = Task.objects.filter(created_at__gte=last_date)
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('weekly_reports/report' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    headings = ['Task Name', 'Description', 'Created At', 'Modified At', 'Status']
    for i in headings:
        worksheet.write(row, col, i)
        col += 1
    col = 0
    row = 1
    for val in tasks:
        worksheet.write(row, col, val.name)
        worksheet.write(row, col + 1, val.description)
        worksheet.write(row, col + 2, val.created_at.strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write(row, col + 3, val.modified_at.strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write(row, col + 4, val.status)
        row += 1

    workbook.close()
    logging.info('stop')