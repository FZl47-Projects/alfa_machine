from django.db.models import Sum, Count, Max
from django.urls import reverse
from django.db import models
from core.models import BaseModel, File


class Department(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_image(self):
        # TODO: should be complete
        pass

    def get_state_busy(self):
        tasks_count = self.task_set.exclude(status__status='finished').count()
        if tasks_count != 0:
            return 'مشغول'
        return 'بیکار'

    def get_absolute_url_manage_tasks(self):
        return reverse('public:task_owner_department', args=(self.id,))

    def get_absolute_url(self):
        return reverse('public:department_detail', args=(self.id,))

    def get_delete_url(self):
        return reverse('departments.general:delete_department', args=(self.id,))

    def get_notifications(self):
        return self.notification_departments.filter(is_showing=True)

    def get_tickets(self):
        return self.ticket_departments.filter(is_open=True)


# TaskMasters model
class TaskMaster(BaseModel):
    title = models.CharField('Task Master name', max_length=128)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.title


class Project(BaseModel):
    STATUS_OPTIONS = (
        ('checking', 'در حال بررسی قبل ساخت'),
        ('under_construction', 'در حال ساخت'),
        ('posted', 'ارسال شده'),
        ('completed', 'تایید و اتمام'),
        ('paused', 'متوقف شده'),
    )
    number_id = models.CharField(max_length=150, null=True, blank=True)
    prepayment_datetime = models.DateTimeField(null=True, blank=True)
    item = models.TextField(null=True, blank=True)
    count_remaining = models.BigIntegerField()
    count_total = models.BigIntegerField()
    has_sample = models.BooleanField(default=False)
    sample_delivery_date = models.DateField(null=True, blank=True)
    mass_delivery_date = models.DateField()
    name = models.CharField(max_length=100)
    task_master = models.ForeignKey(TaskMaster, on_delete=models.CASCADE, related_name='projects')
    time_start = models.DateField(null=True, blank=True)
    time_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    price = models.BigIntegerField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='under_construction')
    inquiry = models.OneToOneField('Inquiry', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'control_project_user'):
            return True
        return False

    def get_state_label(self):
        pr = self.get_progress_percentage()
        if pr == 100:
            return 'تمام شده'
        return 'در حال انجام'

    def get_has_sample_state(self):
        if self.has_sample:
            return 'دارد'
        return 'ندارد'

    def get_progress_percentage(self):
        try:
            all_count = self.get_tasks().count()
            finished_count = self.get_tasks().filter(state='finished').count()
            p = (100 / all_count) * finished_count
            return round(p, 1)
        except:
            return 0

    def get_absolute_url(self):
        return reverse('public:project_detail', args=(self.id,))

    def get_tasks(self):
        return self.task_set.all()

    def get_files(self):
        return self.projectfile_set.order_by('-id')

    def get_tasks_progress(self):
        return self.get_tasks().filter(state='progress')

    def get_tasks_queue(self):
        return self.get_tasks().filter(state='queue')

    def get_tasks_need_to_check(self):
        return self.get_tasks().filter(state='need-to-check')

    def get_tasks_need_to_replan(self):
        return self.get_tasks().filter(state='need-to-replan')

    def get_tasks_hold(self):
        return self.get_tasks().filter(state='hold')

    def get_tasks_finished(self):
        return self.get_tasks().filter(state='finished')

    def get_notifications(self):
        return self.notificationdepartment_set.all()

    def get_prepayment(self):
        p = self.prepayment_set.first()
        return p

    def get_last_payment(self):
        p = self.payment_set.first()
        return p

    def get_payments_price(self):
        payments = self.payment_set.all().aggregate(p=Sum('price'))['p'] or 0
        pre_payments = self.prepayment_set.all().aggregate(p=Sum('price'))['p'] or 0
        return pre_payments + payments

    def get_payments(self):
        return self.payment_set.all()

    def get_prepayments(self):
        return self.prepayment_set.all()

    def get_warehouse_registrations(self):
        try:
            return self.warehouse_registrations.all()
        except (AttributeError, TypeError):
            return []

    def get_tickets(self):
        tickets = self.ticketdepartment_set.values('description').annotate(count=Count('description'))
        unique_tickets = []

        for ticket in tickets:
            obj = self.ticketdepartment_set.filter(description=ticket['description']).first()
            unique_tickets.append(obj)

        return unique_tickets

    def get_prepayment_datetime(self):
        if self.prepayment_datetime:
            return self.prepayment_datetime.strftime('%Y-%m-%d %H:%M')
        return ''

    def get_sample_delivery_date(self):
        if not self.sample_delivery_date:
            return ''
        return self.sample_delivery_date.strftime('%Y-%m-%d %H:%M')

    def get_mass_delivery_date(self):
        return self.mass_delivery_date.strftime('%Y-%m-%d %H:%M')

    def get_mass_delivery_date_input(self):
        return self.mass_delivery_date.strftime('%Y-%m-%d')

    def get_sample_delivery_date_input(self):
        if not self.sample_delivery_date:
            return ''
        return self.sample_delivery_date.strftime('%Y-%m-%d')

    def get_prepayment_datetime_input(self):
        if self.prepayment_datetime:
            return self.prepayment_datetime.strftime('%Y-%m-%d')
        return ''

    def get_time_end_input(self):
        if self.time_end:
            return self.time_end.strftime('%Y-%m-%d')
        return ''

    def get_time_start_input(self):
        if self.time_start:
            return self.time_start.strftime('%Y-%m-%d')
        return ''


class ProjectFile(BaseModel, File):
    name = models.CharField(max_length=100)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    from_department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name


class Task(BaseModel, File):
    # STATUS_OPTIONS = (
    #     ('finished', 'انجام شد'),
    #     ('follow-up', 'پیگیری'),
    #     ('allocation', 'تخصیص'),
    # )
    STATE_OPTIONS = (
        ('finished', 'انجام شد'),
        ('progress', 'در حال انجام'),
        ('queue', 'در صف'),
        ('hold', 'نگه داشته شده'),
        ('need-to-check', 'نیاز به بررسی'),
        ('need-to-replan', 'نیاز به برنامه ریزی مجدد'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    # status = models.CharField(max_length=20, choices=STATUS_OPTIONS,default='allocation')
    state = models.CharField(max_length=20, choices=STATE_OPTIONS, default='queue')
    state_modify_time = models.DateTimeField(null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    from_department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='from_department')
    to_department = models.ForeignKey('Department', on_delete=models.CASCADE)
    allocator_user = models.ForeignKey('account.User', on_delete=models.CASCADE)  # who created task
    work_time = models.CharField(max_length=64, null=True, blank=True)
    time_start = models.DateField(null=True)
    time_end = models.DateField(null=True)
    priority = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = 'priority', '-id',

    def __str__(self):
        return self.name

    def get_state_label(self):
        return self.get_state_display()

    def get_absolute_url(self):
        return reverse('public:task_detail', args=(self.id,))

    def get_state_modify_time(self):
        if not self.state_modify_time:
            return
        return self.state_modify_time.strftime('%Y-%m-%d %H:%M')

    def get_time_start(self):
        if not self.time_start:
            return
        return self.time_start.strftime('%Y-%m-%d')

    def get_time_end(self):
        if not self.time_end:
            return
        return self.time_end.strftime('%Y-%m-%d')


class TaskStatus(BaseModel, File):
    STATUS_OPTIONS = (
        ('accepted', 'تایید شد'),
        ('rejected', 'رد شد'),
    )
    allocator_user = models.ForeignKey('account.User', on_delete=models.CASCADE)  # who accept or rejected task
    task = models.OneToOneField('Task', on_delete=models.CASCADE, related_name='status')
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS)
    description = models.TextField()

    def __str__(self):
        return self.status


class Inquiry(BaseModel):
    STATE_OPTIONS = (
        ('canceled', 'انصراف'),
        ('waiting_for_price', 'در انتظار قیمت'),
        ('price_recorded', 'قیمت ارسال شده'),
    )
    from_department = models.ForeignKey('Department', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    number_id = models.CharField(max_length=32, null=True, blank=True)
    state = models.CharField(max_length=32, choices=STATE_OPTIONS, default='waiting_for_price', blank=True)
    sender = models.ForeignKey(TaskMaster, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    time_receive = models.DateField(null=True, blank=True)
    time_deadline_response = models.DateField(null=True, blank=True)
    time_submit = models.DateField(null=True, blank=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.title

    def get_status(self):
        status = getattr(self, 'status', None)
        if not status:
            return 'درحال بررسی'

        if status.status == 'accepted':
            return 'تایید شده'
        elif status.status == 'rejected':
            return 'رد شده'

    def get_time_submited(self):
        if self.time_submit:
            return self.time_submit.strftime('%Y-%m-%d')

    def get_files(self):
        return self.inquiryfile_set.all().order_by('-id')

    def get_absolute_url(self):
        return f"{reverse('public:inquiry')}?search={self.number_id}"


class InquiryStatus(BaseModel, File):
    STATUS_OPTIONS = (
        ('accepted', 'تایید شد'),
        ('rejected', 'رد شد'),
    )
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS)
    inquiry = models.OneToOneField('Inquiry', on_delete=models.CASCADE, related_name='status')
    description = models.TextField()

    def __str__(self):
        return self.status


class InquiryFile(BaseModel, File):
    name = models.CharField(max_length=100)
    inquiry = models.ForeignKey('Inquiry', on_delete=models.CASCADE)
    description = models.TextField(null=True)
    from_department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True, related_name='inquiry_file')
    departments = models.ManyToManyField('Department')  # departments can access to this file

    def __str__(self):
        return f'{self.name} - {self.inquiry} - File'

    def get_department_ids(self):
        return list(self.departments.values_list('id', flat=True))
