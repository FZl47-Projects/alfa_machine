from django.db.models import Sum
from django.urls import reverse
from django.db import models
from django.db.models import F, Max
from core.models import BaseModel, FileAbstract

from django_jalali.db import models as jmodels


class Department(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'control_project_user'):
            return True
        return False

    @classmethod
    def has_perm_to_delete(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user',):
            return True
        return False

    def get_users(self):
        return self.user_set.all()

    def get_absolute_url(self):
        return reverse('public:department__detail', args=(self.id,))

    def get_notifications(self):
        return self.to_dp_notification.all()

    def get_unread_notifications(self):
        return self.get_notifications().filter(seen_status=None)

    def get_tickets(self):
        return self.from_dep_ticket.filter(is_open=True)

    def get_tasks(self):
        return self.task_set.all()

    def get_tasks_by_last_status(self):
        return self.get_tasks().annotate(last_status=Max('taskstatus__id'))

    def get_tasks_finished(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='finished',
                                                      taskstatus__id__gte=F('last_status'))

    def get_tasks_queue(self):
        tasks = self.get_tasks_by_last_status().filter(taskstatus__status='queue',
                                                       taskstatus__id__gte=F('last_status')) \
                | self.get_tasks().filter(taskstatus=None)
        return tasks.distinct()

    def get_tasks_progress(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='progress',
                                                      taskstatus__id__gte=F('last_status'))

    def get_tasks_hold(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='hold',
                                                      taskstatus__id__gte=F('last_status'))

    def get_tasks_need_to_check(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='need-to-check',
                                                      taskstatus__id__gte=F('last_status'))

    def get_tasks_need_to_replan(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='need-to-replan',
                                                      taskstatus__id__gte=F('last_status'))

    def get_tasks_remaining(self):
        return self.get_tasks().exclude(taskstatus__status='finished')


class TaskMaster(BaseModel):
    name = models.CharField('Task Master name', max_length=128)
    description = models.TextField(null=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'):
            return True
        return False

    @classmethod
    def has_perm_to_delete(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user',):
            return True
        return False

    def get_absolute_url(self):
        return reverse('public:task_master__detail', args=(self.id,))

    def get_projects(self):
        return self.projects.all()

    def get_inquiries(self):
        return self.inquiry_set.all()


class ProjectStep(BaseModel):
    PERSON_TRAFFIC_OPTIONS = (
        ('person/day', 'نفر/روز'),
        ('person/hour', 'نفر/ساعت'),
    )

    name = models.CharField(max_length=100)
    from_department = models.ForeignKey('Department', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    person_traffic = models.CharField(max_length=15, choices=PERSON_TRAFFIC_OPTIONS)
    plan = models.IntegerField()
    actual = models.IntegerField(null=True)
    description = models.TextField(null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'control_project_user'):
            return True
        return False

    def get_absolute_url(self):
        return reverse('public:project_step__detail', args=(self.id,))

    def get_person_traffic_label(self):
        return self.get_person_traffic_display()

    def get_status_result(self):
        if self.actual:
            return self.plan - self.actual
        return None


class ProjectNote(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.text[:20]


class Project(BaseModel):
    # TODO: (refactor) add manager for handle active project and ..

    STATUS_OPTIONS = (
        ('checking', 'در حال بررسی قبل ساخت'),
        ('under_construction', 'در حال ساخت'),
        ('posted', 'ارسال شده'),
        ('completed', 'تایید و اتمام'),
        ('paused', 'متوقف شده'),
    )
    number_id = models.CharField(max_length=150, null=True, blank=True)
    item = models.TextField(null=True, blank=True)
    count_remaining = models.BigIntegerField()
    count_total = models.BigIntegerField()
    has_sample = models.BooleanField(default=False)
    sample_delivery_date = jmodels.jDateField(null=True, blank=True)
    mass_delivery_date = jmodels.jDateField(null=True, blank=True)
    name = models.CharField(max_length=100)
    task_master = models.ForeignKey(TaskMaster, on_delete=models.CASCADE, related_name='projects')
    time_start = jmodels.jDateField(null=True, blank=True)
    time_end = jmodels.jDateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='under_construction')
    inquiry = models.OneToOneField('Inquiry', on_delete=models.SET_NULL, null=True, blank=True)
    progress_percentage = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.name

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'control_project_user'):
            return True
        return False

    @classmethod
    def has_perm_to_steps(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'control_project_user'):
            return True
        return False

    @classmethod
    def has_perm_to_financial_amount(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'financial_user'):
            return True
        return False

    @classmethod
    def has_perm_to_warehouse_amount(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'control_project_user', 'financial_user', 'commerce_user', 'warehouse_user'):
            return True
        return False

    def get_state_label(self):
        pr = self.get_progress_percentage()
        if pr == 100:
            return 'تمام شده'
        return 'در حال انجام'

    def get_status_label(self):
        return self.get_status_display()

    def get_has_sample_state(self):
        if self.has_sample:
            return 'دارد'
        return 'ندارد'

    def get_steps(self):
        return self.projectstep_set.all()

    def get_last_step(self):
        return self.get_steps().first()

    def get_progress_percentage(self):
        return self.progress_percentage

    def get_image_cover_url(self):
        LIST_IMAGES = [
            'bg-black.png',
            'bg-blue.png',
            'bg-creamy.png',
            'bg-gray.png',
            'bg-green.png',
            'bg-light-purple.png',
            'bg-purple.png',
            'bg-pink.png',
            'bg-red.png',
            'bg-yellow.png',
        ]
        try:
            n = LIST_IMAGES[int(str(self.id)[-1])]
            return f'/static/frontend/images/colors/{n}'
        except Exception as e:
            return '/static/frontend/images/colors/bg-creamy.png'

    def get_absolute_url(self):
        return reverse('public:project__detail', args=(self.id,))

    def get_notes(self, user):
        return self.projectnote_set.filter(user=user)

    def get_comments(self):
        return self.projectcomment_set.all()

    def get_tasks(self):
        return self.task_set.all()

    def get_tasks_by_last_status(self):
        return self.get_tasks().annotate(last_status=Max('taskstatus__id'))

    def get_files(self):
        return self.projectfile_set.order_by('-id')

    def get_tasks_progress(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='progress',
                                                      taskstatus__id__gte=F('last_status'))

    def get_tasks_queue(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='queue',
                                                      taskstatus__id__gte=F('last_status'))

    def get_tasks_need_to_check(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='need-to-check',
                                                      taskstatus__id__gte=F('last_status'))

    def get_tasks_need_to_replan(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='need-to-replan',
                                                      taskstatus__id__gte=F('last_status'))

    def get_tasks_hold(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='hold', taskstatus__id__gte=F('last_status'))

    def get_tasks_finished(self):
        return self.get_tasks_by_last_status().filter(taskstatus__status='finished',
                                                      taskstatus__id__gte=F('last_status'))

    def get_notifications(self):
        return self.notificationdepartment_set.all()

    def get_last_payment(self):
        p = self.payment_set.first()
        return p

    def get_total_payments_amount(self):
        payments = self.get_payments().aggregate(p=Sum('price'))['p'] or 0
        return payments

    def get_total_prepayments_amount(self):
        payments = self.get_prepayments().aggregate(p=Sum('price'))['p'] or 0
        return payments

    def get_payments(self):
        return self.payment_set.all()

    def get_prepayments(self):
        return self.get_payments().filter(type_payment='prepayment')

    def get_total_warehouse_items_amount(self):
        t = self.get_warehouse_items().aggregate(p=Sum('price'))['p'] or 0
        return t

    def get_warehouse_items(self):
        return self.itemwarehouse_set.all()

    def get_participating_departments(self):
        departments = Department.objects.filter(task__project=self).distinct()
        return departments

    def get_remaining_time_end(self):
        return self.get_remaining_date_field(self.time_end)

    def get_remaining_mass_delivery(self):
        return self.get_remaining_date_field(self.mass_delivery_date)

    def get_remaining_sample_delivery(self):
        return self.get_remaining_date_field(self.mass_delivery_date)


class ProjectFile(BaseModel, FileAbstract):
    name = models.CharField(max_length=100)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='task_files')
    allocator_user = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True)
    from_department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    to_departments = models.ManyToManyField('Department', related_name='departments_access')
    description = models.TextField(null=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.name

    def has_perm_to_modify(self, user):
        if user.is_anonymous:
            return False
        if ((user == self.allocator_user) and (user.department in self.get_to_departments())) or (
                user.role in ('super_user',)):
            return True
        return False

    def get_absolute_url(self):
        return reverse('public:project_file__detail', args=(self.id,))

    def get_to_departments(self):
        return self.to_departments.all()


class ProjectComment(BaseModel):
    from_department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='project_comment_from_dp')
    to_departments = models.ManyToManyField('Department', related_name='project_comment_to_dp')
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.text[:10]

    def has_perm_to_modify(self, user):
        if user.is_anonymous:
            return False
        if user.department == self.from_department:
            return True
        return False


class Task(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    from_department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='from_department')
    to_department = models.ForeignKey('Department', on_delete=models.CASCADE)
    allocator_user = models.ForeignKey('account.User', on_delete=models.CASCADE)  # who created task
    time_start = jmodels.jDateField(null=True, blank=True)
    time_end = jmodels.jDateField(null=True, blank=True)
    priority = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = 'priority', '-id',

    def __str__(self):
        return self.name

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'control_project_user'):
            return True
        return False

    @classmethod
    def has_perm_to_send_notify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'control_project_user'):
            return True
        return False

    def get_absolute_url(self):
        return reverse('public:task__detail', args=(self.id,))

    def get_statuses(self):
        return self.taskstatus_set.all()

    def get_last_status(self):
        return self.get_statuses().first()

    def get_status_label(self):
        s = self.get_last_status()
        if s:
            return s.get_status_label()
        return 'در صف'

    def get_remaining_time(self):
        return self.get_remaining_date_field(self.time_end)

    def get_files(self):
        return self.task_files.all()


class TaskStatus(BaseModel, FileAbstract):
    STATUS_OPTIONS = (
        ('finished', 'انجام شد'),
        ('progress', 'در حال انجام'),
        ('queue', 'در صف'),
        ('hold', 'نگه داشته شده'),
        ('need-to-check', 'نیاز به بررسی'),
        ('need-to-replan', 'نیاز به برنامه ریزی مجدد'),
    )
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    allocator_user = models.ForeignKey('account.User', null=True, on_delete=models.SET_NULL)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS)
    description = models.TextField(null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"{self.status} - {self.task}"

    def get_status_label(self):
        return self.get_status_display()


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
    task_master = models.ForeignKey(TaskMaster, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    time_receive = jmodels.jDateField(null=True, blank=True)
    time_deadline_response = jmodels.jDateField(null=True, blank=True)
    time_submit = jmodels.jDateField(null=True, blank=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return self.title

    @classmethod
    def has_perm_to_modify(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user', 'commerce_user', 'procurement_commerce_user'):
            return True
        return False

    @classmethod
    def has_perm_to_manage_status(cls, user):
        if user.is_anonymous:
            return False
        if user.role in ('super_user',):
            return True
        return False

    def get_state_label(self):
        return self.get_state_display()

    def get_status_label(self):
        status = getattr(self, 'status', None)
        if not status:
            return 'درحال بررسی'

        if status.status == 'accepted':
            return 'تایید شده'
        elif status.status == 'rejected':
            return 'رد شده'

    def get_project(self):
        return getattr(self, 'project', None)

    def get_files(self):
        return self.inquiryfile_set.all()

    def get_absolute_url(self):
        return reverse('public:inquiry__detail', args=(self.id,))

    def get_referral_to_project_url(self):
        return f"{reverse('public:project__add')}?inquiry-id={self.id}"

    def get_remaining_deadline(self):
        return self.get_remaining_date_field(self.time_deadline_response)


class InquiryStatus(BaseModel, FileAbstract):
    STATUS_OPTIONS = (
        ('accepted', 'تایید شده'),
        ('rejected', 'رد شده'),
    )
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS)
    inquiry = models.OneToOneField('Inquiry', on_delete=models.CASCADE, related_name='status')
    description = models.TextField()

    def __str__(self):
        return self.status


class InquiryFile(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    files = models.ManyToManyField('File')
    inquiry = models.ForeignKey('Inquiry', on_delete=models.CASCADE)
    allocator_user = models.ForeignKey('account.User', null=True, on_delete=models.SET_NULL)
    from_department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True,
                                        related_name='inquiry_file_from_dep')
    to_departments = models.ManyToManyField('Department',
                                            related_name='inquiry_file_to_dep')  # departments can access to this file

    def __str__(self):
        return f'{self.name} - {self.inquiry} - File'

    def get_department_ids(self):
        return list(self.to_departments.values_list('id', flat=True))

    def get_files(self):
        return self.files.all()

    def get_to_departments(self):
        return self.to_departments.all()


class File(FileAbstract):
    class Meta:
        ordering = ('-id',)
