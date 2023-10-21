from django.db import models
from django.db.models import Sum
from django.urls import reverse
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
        return self.notificationdepartment_set.filter(is_showing=True)


class Project(BaseModel):
    STATUS_OPTIONS = (
        ('paused', 'متوقف شده'),
        ('under_construction', 'در حال ساخت'),
    )
    number_id = models.IntegerField()
    prepayment_datetime = models.DateTimeField()
    item = models.TextField(null=True)
    count_remaining = models.BigIntegerField()
    count_total = models.BigIntegerField()
    sample_delivery_date = models.DateField()
    mass_delivery_date = models.DateField()
    name = models.CharField(max_length=100)
    task_master = models.CharField(max_length=100)
    time_start = models.DateField()
    time_end = models.DateField()
    is_active = models.BooleanField(default=True)
    price = models.BigIntegerField()
    is_paid = models.BooleanField(default=False)
    description = models.TextField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='under_construction')

    def __str__(self):
        return self.name

    def get_state_label(self):
        pr = self.get_progress_percentage()
        if pr == 100:
            return 'تمام شده'
        return 'در حال انجام'

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

    def get_tasks_progress(self):
        return self.get_tasks().filter(state='progress')

    def get_tasks_queue(self):
        return self.get_tasks().filter(state='queue')

    def get_tasks_finished(self):
        return self.get_tasks().filter(state='finished')

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

    def get_material_items(self):
        try:
            return self.materialproject.items.all()
        except:
            return []

    def get_files(self):
        return self.projectfile_set.all()

    def get_tickets(self):
        return self.ticketdepartment_set.all()

    def get_prepayment_datetime(self):
        return self.prepayment_datetime.strftime('%Y-%m-%d %H:%M')

    def get_sample_delivery_date(self):
        return self.sample_delivery_date.strftime('%Y-%m-%d %H:%M')

    def get_mass_delivery_date(self):
        return self.mass_delivery_date.strftime('%Y-%m-%d %H:%M')

    def get_mass_delivery_date_input(self):
        return self.mass_delivery_date.strftime('%Y-%m-%d')

    def get_sample_delivery_date_input(self):
        return self.sample_delivery_date.strftime('%Y-%m-%d')

    def get_prepayment_datetime_input(self):
        return self.prepayment_datetime.strftime('%Y-%m-%d')

    def get_time_end_input(self):
        return self.time_end.strftime('%Y-%m-%d')

    def get_time_start_input(self):
        return self.time_start.strftime('%Y-%m-%d')


class ProjectFile(BaseModel, File):
    name = models.CharField(max_length=100)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    description = models.TextField()

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
    description_allocate = models.TextField(null=True, blank=True)
    # status = models.CharField(max_length=20, choices=STATUS_OPTIONS,default='allocation')
    state = models.CharField(max_length=20, choices=STATE_OPTIONS, default='queue')
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    from_department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='from_department')
    to_department = models.ForeignKey('Department', on_delete=models.CASCADE)
    allocator_user = models.ForeignKey('account.User', on_delete=models.CASCADE)  # who created task
    work_hour = models.IntegerField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
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

    def get_time_start(self):
        return self.time_start.strftime('%Y-%m-%d')

    def get_time_end(self):
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
    from_department = models.ForeignKey('Department', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    time_submited = models.DateTimeField()

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.title

    def get_status(self):
        status = getattr(self, 'status', None)
        if status:
            return status.status
        return 'progress'

    def get_time_submited(self):
        return self.time_submited.strftime('%Y-%m-%d %H:%M')


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
