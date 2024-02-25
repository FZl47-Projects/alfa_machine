import jdatetime
from django.db import models
from core.utils import get_time, get_timesince_persian
from .mixins import RemoveOldFileMixin


def upload_file_src(instance, path):
    path = str(path).split('.')
    frmt = path[-1]
    file_name = path[0]
    tm = get_time('%Y-%m-%d')
    return f'files/{tm}/{file_name}.{frmt}'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_updated_at(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_created_at_date(self):
        return self.created_at.strftime('%Y-%m-%d')

    def get_created_at_timepast(self):
        return get_timesince_persian(self.created_at)

    def get_updated_at_timepast(self):
        return get_timesince_persian(self.updated_at)

    def get_remaining_date_field(self, date_field):
        # remaining time by days
        if date_field:
            t = jdatetime.date(date_field.year, date_field.month, date_field.day) - jdatetime.date.today()
            return t.days
        return '-'


class FileAbstract(RemoveOldFileMixin, models.Model):
    FIELDS_REMOVE_FILES = ('file',)

    file = models.FileField(upload_to=upload_file_src, max_length=400, null=True, blank=True)

    class Meta:
        ordering = '-id',
        abstract = True

    def __str__(self):
        return f'#{self.id} File'

    def get_file_url(self):
        try:
            return self.file.url
        except:
            return None
