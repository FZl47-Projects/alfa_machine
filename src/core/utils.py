import string
import random
import datetime
from django.utils import timezone
from django.core.mail import send_mail as _send_email_django
from django.conf import settings
from django_q.tasks import async_task
from django.contrib import messages


def random_str(size=15, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_int(size: int = 5):
    new_code = ''.join([str(random.randint(0, 9)) for _ in range(size)])
    return new_code


def get_time(frmt='%Y-%m-%d_%H:%M'):
    t = timezone.now()
    if frmt is not None:
        t = t.strftime(frmt)
    return t


def get_timesince_persian(time, time_base=None):
    if not time_base:
        time_base = get_time(None)
    diff_time = datetime.datetime(time_base.year, time_base.month, time_base.day, time_base.hour,
                                  time_base.minute) - datetime.datetime(time.year, time.month, time.day, time.hour,
                                                                        time.minute)

    diff_time_sec = diff_time.total_seconds()
    # sec = diff_time_sec % 60
    min = int(diff_time_sec // 60 % 60)
    hour = int(diff_time_sec // 3600)
    day = diff_time.days
    if min > 0:
        result = f'{min} دقیقه پیش'
    else:
        result = f'لحظاتی پیش'

    if hour > 0:
        result = f'{hour} ساعت پیش'

    if day > 0:
        result = f'{day}  روز پیش'

    return result


def get_datesince_persian(date, time_base=None):
    if not time_base:
        time_base = get_time(None)
    diff_time = datetime.datetime(time_base.year, time_base.month, time_base.day) - datetime.datetime(date.year, date.month, date.day)

    diff_time_sec = diff_time.total_seconds()
    # sec = diff_time_sec % 60
    min = int(diff_time_sec // 60 % 60)
    day = diff_time.days
    if min > 0:
        result = f'{min} دقیقه پیش'
    else:
        result = f'لحظاتی پیش'

    if day > 0:
        result = f'{day}  روز پیش'

    return result


def send_email(email, content, **kwargs):
    # send email in background 
    async_task(_send_email_django,
               settings.EMAIL_SUBJECT,
               content,
               settings.EMAIL_HOST_USER,
               [email]
               )


def add_prefix_phonenum(phonenumber):
    return f'+98{phonenumber}'


def form_validate_err(request, form):
    if form.is_valid() is False:
        errors = form.errors.as_data()
        messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
        # if errors:
        #     errors = list(errors.values())
        #     err = str(errors[0][0])
        #     err = err.replace('[', '').replace(']', '')
        #     err = err.replace("'", '')
        #     messages.error(request, err)
        # else:
        #     messages.error(request, 'دیتای ورودی نامعتبر است')
        return False
    return True
