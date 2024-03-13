import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib import messages
from django.db.models import Q, Count
from core.utils import form_validate_err
from account.auth.decorators import user_role_required_cbv
from notification.utils import create_notification
from public import models, forms


def err_403_handler(request, exception):
    return render(request, 'public/errors/403.html')


def err_404_handler(request, exception):
    return render(request, 'public/errors/404.html')


def err_500_handler(request):
    return render(request, 'public/errors/500.html')


class Index(View):
    def get(self, request):
        return redirect(request.user.get_absolute_url_dashboard())


class ProjectDetail(LoginRequiredMixin, View):
    template_name = 'public/project/detail.html'

    def get(self, request, project_id):
        user_dp = request.user.department
        project = get_object_or_404(models.Project, id=project_id)
        steps = project.get_steps()
        comments = project.get_comments()
        comments = (comments.filter(from_department=user_dp) | comments.filter(to_departments__in=[user_dp])).distinct()
        data_chart_step_1 = list(steps.filter(person_traffic='person/day').values('name', 'plan', 'actual'))
        data_chart_step_2 = list(steps.filter(person_traffic='person/hour').values('name', 'plan', 'actual'))

        context = {
            'project': project,
            'steps': steps,
            'comments': comments,
            'notes': project.get_notes(request.user),
            'task_masters': models.TaskMaster.objects.all(),
            'departments': models.Department.objects.all(),
            # chart data
            'data_chart_step_1': json.dumps(data_chart_step_1),
            'data_chart_step_2': json.dumps(data_chart_step_2),
            # permissions
            'has_perm_to_modify': project.has_perm_to_modify(request.user),
            'has_perm_to_steps': project.has_perm_to_steps(request.user),
            'has_perm_to_financial_amount': project.has_perm_to_financial_amount(request.user),
            'has_perm_to_warehouse_amount': project.has_perm_to_warehouse_amount(request.user),
        }
        return render(request, self.template_name, context)


class ProjectList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/project/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def filter(self, projects):
        qs = self.request.GET
        search = qs.get('search', None)
        task_master = qs.get('task_master', 'all')
        project_status = qs.get('project_status', 'all')

        if search:
            projects = projects.filter(name__icontains=search)

        if (task_master != 'all') and (task_master.isdigit()):
            projects = projects.filter(task_master_id=task_master)

        if project_status != 'all':
            projects = projects.filter(status=project_status)

        # filter by start and end date project
        time_start_gt = qs.get('time_start__gt', None)
        time_start_lt = qs.get('time_start__lt', None)
        time_end_gt = qs.get('time_end__gt', None)
        time_end_lt = qs.get('time_end__lt', None)

        if time_start_gt:
            projects = projects.filter(time_start__gt=time_start_gt)

        if time_start_lt:
            projects = projects.filter(time_start__lt=time_start_lt)

        if time_end_gt:
            projects = projects.filter(time_end__gt=time_end_gt)

        if time_end_lt:
            projects = projects.filter(time_end__lt=time_end_lt)

        return projects

    def get(self, request):
        projects = models.Project.objects.filter(is_active=True)
        projects = self.filter(projects)
        pagination, projects = self.pagination(projects)
        context = {
            'projects': projects,
            'pagination': pagination,
            'task_masters': models.TaskMaster.objects.all()
        }
        return render(request, self.template_name, context)


class ProjectAdd(LoginRequiredMixin, View):
    template_name = 'public/project/add.html'

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def get(self, request):
        context = {
            'task_masters': models.TaskMaster.objects.all()
        }
        inquiry_id = request.GET.get('inquiry-id', None)
        if inquiry_id:
            context['inquiry'] = models.Inquiry.objects.get(id=inquiry_id, project=None)

        return render(request, self.template_name, context)

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def post(self, request):
        data = request.POST
        f = forms.ProjectCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('public:project__add')
        project = f.save()
        messages.success(request, 'پروژه با موفقیت ایجاد شد')
        return redirect(project.get_absolute_url())


class ProjectUpdate(LoginRequiredMixin, View):

    def post(self, request, project_id):
        project = get_object_or_404(models.Project, id=project_id)
        if not project.has_perm_to_modify(request.user):
            raise PermissionDenied
        f = forms.ProjectUpdate(data=request.POST, instance=project)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(project.get_absolute_url())
        f.save()
        messages.success(request, 'پروژه با موفقیت بروزرسانی شد')
        return redirect(project.get_absolute_url())


class ProjectDelete(LoginRequiredMixin, View):

    def get(self, request, project_id):
        if not models.Project.has_perm_to_modify(request.user):
            raise PermissionDenied
        project = get_object_or_404(models.Project, id=project_id)
        project.delete()
        messages.success(request, 'پروژه با موفقیت حذف شد')
        return redirect('public:project__list')


class ProjectCommentAdd(LoginRequiredMixin, View):

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST.copy()
        # set additional values
        data['from_department'] = request.user.department
        f = forms.ProjectCommentCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect(referer_url)
        comment = f.save()
        messages.success(request, 'نظر با موفقیت ثبت شد')
        return redirect(comment.project.get_absolute_url())


class ProjectCommentDelete(LoginRequiredMixin, View):

    def get(self, request, comment_id):
        comment = get_object_or_404(models.ProjectComment, id=comment_id)
        comment.delete()
        messages.success(request, 'نظر با موفقیت حذف شد')
        return redirect(comment.project.get_absolute_url())


class ProjectNoteAdd(LoginRequiredMixin, View):

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST.copy()
        # set additional values
        data['user'] = request.user
        f = forms.ProjectNoteCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect(referer_url)
        note = f.save()
        messages.success(request, 'یادداشت با موفقیت ایجاد شد')
        return redirect(note.project.get_absolute_url())


class ProjectNoteDelete(LoginRequiredMixin, View):

    def get(self, request, note_id):
        note = get_object_or_404(models.ProjectNote, id=note_id)
        note.delete()
        messages.success(request, 'یادداشت با موفقیت حذف شد')
        return redirect(note.project.get_absolute_url())


class ProjectStepAdd(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user
        if not models.Project.has_perm_to_steps(user):
            raise PermissionDenied
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST.copy()
        # set additional values
        data['from_department'] = user.department
        f = forms.ProjectStepCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect(referer_url)
        step = f.save()
        messages.success(request, 'مرحله با موفقیت ایجاد شد')
        return redirect(step.project.get_absolute_url())


class ProjectStepDetail(LoginRequiredMixin, View):
    template_name = 'public/project_step/detail.html'

    def get(self, request, step_id):
        user = request.user
        if not models.Project.has_perm_to_steps(user):
            raise PermissionDenied
        step = get_object_or_404(models.ProjectStep, id=step_id)
        context = {
            'step': step,
            # permissions
            'has_perm_to_modify': step.has_perm_to_modify(user)
        }
        return render(request, self.template_name, context)


class ProjectStepDelete(LoginRequiredMixin, View):

    def get(self, request, step_id):
        user = request.user
        if not models.Project.has_perm_to_modify(user):
            raise PermissionDenied
        step = get_object_or_404(models.ProjectStep, id=step_id)
        step.delete()
        messages.success(request, 'مرحله پروژه با موفقیت حذف شد')
        return redirect(step.project.get_absolute_url())


class ProjectStepUpdate(LoginRequiredMixin, View):

    def post(self, request, step_id):
        user = request.user
        if not models.Project.has_perm_to_modify(user):
            raise PermissionDenied
        step = get_object_or_404(models.ProjectStep, id=step_id)
        f = forms.ProjectStepUpdate(data=request.POST, instance=step)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(step.get_absolute_url())
        f.save()
        messages.success(request, 'مرحله پروژه با موفقیت بروزرسانی شد')
        return redirect(step.get_absolute_url())


class TaskAdd(LoginRequiredMixin, View):
    template_name = 'public/task/add.html'

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request):
        context = {
            'projects': models.Project.objects.filter(is_active=True),
            'departments': models.Department.objects.all()
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def post(self, request):
        data = request.POST.copy()
        # set default values
        data['allocator_user'] = request.user
        data['from_department'] = request.user.department

        f = forms.TaskCreate(data, request.FILES)
        if not form_validate_err(request, f):
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect('public:task__add')
        task = f.save()
        # create status task(queue)
        models.TaskStatus.objects.create(
            department=task.to_department,
            task=task,
            status='queue',
            description='ایجاد به صورت خودکار'
        )
        # create notification for department
        create_notification(
            'تسک جدید',
            from_department=request.user.department,
            to_departments=[task.to_department],
            projects=[task.project],
            attached_link=task.get_absolute_url(),
        )
        messages.success(request, 'تسک با موفقیت ایجاد شد')
        return redirect(task.get_absolute_url())


class TaskList(LoginRequiredMixin, View):
    USER_ACCESS_TO_ALL = ('super_user', 'control_project_user')
    pagination_count = 25
    template_name = 'public/task/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def get_tasks(self):
        """
            get tasks by user department
        """
        tasks = models.Task.objects.all()
        user = self.request.user
        if user.role in self.USER_ACCESS_TO_ALL:
            return tasks
        tasks = tasks.filter(to_department=user.department)
        return tasks

    def sort(self, tasks):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            tasks = tasks.order_by('-id')
        elif sort_by == 'oldest':
            tasks = tasks.order_by('id')
        elif sort_by == 'priority_high':
            tasks = tasks.order_by('-priority')
        return tasks

    def filter(self, tasks):
        qs = self.request.GET
        search = qs.get('search', None)
        project = qs.get('project', 'all')
        status = qs.get('status', 'all')
        to_department = qs.get('to_department', 'all')

        if search:
            tasks = tasks.filter(name__icontains=search)

        if (project != 'all') and (project.isdigit()):
            tasks = tasks.filter(project_id=project)

        if (to_department != 'all') and (to_department.isdigit()):
            tasks = tasks.filter(to_department_id=to_department)

        if status != 'all':
            if status == 'queue':
                lookup = Q(taskstatus__status=status) | Q(taskstatus=None)
                tasks = tasks.filter(lookup).distinct()
            else:
                tasks = tasks.filter(taskstatus__status=status)

        # filter by start and end date tasks
        time_start_gt = qs.get('time_start__gt', None)
        time_start_lt = qs.get('time_start__lt', None)
        time_end_gt = qs.get('time_end__gt', None)
        time_end_lt = qs.get('time_end__lt', None)

        if time_start_gt:
            tasks = tasks.filter(time_start__gt=time_start_gt)

        if time_start_lt:
            tasks = tasks.filter(time_start__lt=time_start_lt)

        if time_end_gt:
            tasks = tasks.filter(time_end__gt=time_end_gt)

        if time_end_lt:
            tasks = tasks.filter(time_end__lt=time_end_lt)

        return tasks

    def get(self, request):
        tasks = self.get_tasks()
        tasks = self.filter(tasks)
        tasks = self.sort(tasks)
        pagination, tasks = self.pagination(tasks)
        context = {
            'pagination': pagination,
            'tasks': tasks,
            'task_status': models.TaskStatus.STATUS_OPTIONS,
            'projects': models.Project.objects.filter(is_active=True),
            'departments': models.Department.objects.all(),
            # permissions
            'has_perm_to_send_notify': models.Task.has_perm_to_send_notify(request.user)
        }
        return render(request, self.template_name, context)


class TaskDetail(LoginRequiredMixin, View):
    USER_FULL_ACCESS = ('super_user', 'control_project_user')
    template_name = 'public/task/detail.html'

    def get(self, request, task_id):
        user = request.user
        task = get_object_or_404(models.Task, id=task_id)
        if task.to_department != user.department and not (user.role in self.USER_FULL_ACCESS):
            raise PermissionDenied
        context = {
            'task': task,
            'task_status': models.TaskStatus.STATUS_OPTIONS,
            # permissions
            'has_perm_to_modify': task.has_perm_to_modify(request.user),
            'has_perm_to_send_notify': task.has_perm_to_send_notify(request.user)
        }
        return render(request, self.template_name, context)


class TaskDelete(LoginRequiredMixin, View):

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request, task_id):
        task = get_object_or_404(models.Task, id=task_id)
        task.delete()
        messages.success(request, 'تسک با موفقیت حذف شد')
        return redirect('public:task__list')


class TaskUpdate(LoginRequiredMixin, View):

    def post(self, request, task_id):
        if not models.Task.has_perm_to_modify(request.user):
            raise PermissionDenied
        task = get_object_or_404(models.Task, id=task_id)
        f = forms.TaskUpdate(data=request.POST, files=request.FILES, instance=task)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect(task.get_absolute_url())
        task = f.save()
        messages.success(request, 'تسک با موفقیت بروزرسانی شد')
        return redirect(task.get_absolute_url())


class TaskStatusAdd(LoginRequiredMixin, View):

    def post(self, request, task_id):
        user = request.user
        task = get_object_or_404(models.Task, id=task_id, to_department=user.department)
        data = request.POST.copy()
        # set additional values
        data['allocator_user'] = user
        data['department'] = user.department
        data['task'] = task
        f = forms.TaskStatusCreate(data=data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect(task.get_absolute_url())
        task_status = f.save()
        messages.success(request, 'وضعیت تسک با موفقیت ایجاد شد')
        return redirect(task.get_absolute_url())


class TaskRemind(LoginRequiredMixin, View):

    def get(self, request, task_id):
        referer_url = request.META.get('HTTP_REFERER', None)
        task = get_object_or_404(models.Task, id=task_id)
        user = request.user
        if not task.has_perm_to_send_notify(request.user):
            raise PermissionDenied
        # create notification for department
        create_notification(
            'یادآوری انجام تسک',
            from_department=user.department,
            to_departments=[task.to_department],
            projects=[task.project],
            attached_link=task.get_absolute_url(),
            description=f'یادآوری جهت انجام تسک ({task.name})'
        )
        messages.success(request, 'یاداوری تسک با موفقیت انجام شد')
        return redirect(referer_url or task.get_absolute_url())


class InquiryAdd(LoginRequiredMixin, View):
    template_name = 'public/inquiry/add.html'

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user'])
    def get(self, request):
        context = {
            'inquiry_states': models.Inquiry.STATE_OPTIONS,
            'task_masters': models.TaskMaster.objects.all(),
            'departments': models.Department.objects.all()
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user'])
    def post(self, request):
        data = request.POST.copy()
        user = request.user
        user_department = user.department
        # set additional values
        data['from_department'] = user_department

        f = forms.InquiryAdd(data)
        if form_validate_err(request, f) is False:
            return redirect('public:inquiry__add')
        inquiry = f.save()

        # create inquiry file's
        # set additional values
        data['inquiry'] = inquiry
        data['from_department'] = user_department
        data['allocator_user'] = user
        data['name'] = data['file_name']
        data['description'] = data['file_description']
        f = forms.InquiryFile(data, request.FILES)
        if f.is_valid():
            # create and upload files
            files_object = []
            files = request.FILES.getlist('files')
            for file in files:
                files_object.append(models.File(file=file))
            files_object = models.File.objects.bulk_create(files_object)
            inquiry_file = f.save()
            inquiry_file.files.add(*files_object)

        messages.success(request, 'استعلام با موفقیت ایجاد شد')
        return redirect(inquiry.get_absolute_url())


class InquiryList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/inquiry/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def filter(self, inquiries):
        qs = self.request.GET
        search = qs.get('search', None)
        task_master = qs.get('task_master', 'all')
        state = qs.get('state', 'all')

        if search:
            lookup = Q(title__icontains=search)
            if search.isdigit():
                lookup = lookup | Q(number_id=search)
            inquiries = inquiries.filter(lookup)

        if (task_master != 'all') and (task_master.isdigit()):
            inquiries = inquiries.filter(task_master_id=task_master)

        if state != 'all':
            inquiries = inquiries.filter(state=state)

        # filter by time
        time_deadline_response_gt = qs.get('time_deadline_response__gt', None)
        time_deadline_response_lt = qs.get('time_deadline_response__lt', None)
        time_submit_gt = qs.get('time_submit__gt', None)
        time_submit_lt = qs.get('time_submit__lt', None)

        if time_deadline_response_gt:
            inquiries = inquiries.filter(time_deadline_response_gt=time_deadline_response_gt)

        if time_deadline_response_lt:
            inquiries = inquiries.filter(time_deadline_response_lt=time_deadline_response_lt)

        if time_submit_gt:
            inquiries = inquiries.filter(time_submit_gt=time_submit_gt)

        if time_submit_lt:
            inquiries = inquiries.filter(time_submit_lt=time_submit_lt)

        return inquiries

    def sort(self, inquiries):
        sort_by = self.request.GET.get('sort_by', 'latest')

        if sort_by == 'latest':
            inquiries = inquiries.order_by('-id')
        elif sort_by == 'oldest':
            inquiries = inquiries.order_by('id')
        return inquiries

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'financial_user'])
    def get(self, request):
        inquiries = models.Inquiry.objects.all()
        inquiries = self.filter(inquiries)
        inquiries = self.sort(inquiries)
        pagination, inquiries = self.pagination(inquiries)

        context = {
            'pagination': pagination,
            'inquiries': inquiries,
            'departments': models.Department.objects.all(),
            'task_masters': models.TaskMaster.objects.all(),
            'inquiry_states': models.Inquiry.STATE_OPTIONS,
        }

        return render(request, self.template_name, context)


class InquiryDetail(LoginRequiredMixin, View):
    template_name = 'public/inquiry/detail.html'

    def get_inquiry_files(self, inquiry):
        department = self.request.user.department
        # get file for this department
        lookup = Q(from_department=department) | Q(to_departments__in=[department])
        files = inquiry.get_files().filter(lookup).distinct()
        return files

    def get(self, request, inquiry_id):
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        context = {
            'inquiry': inquiry,
            'inquiry_files': self.get_inquiry_files(inquiry),
            'task_masters': models.TaskMaster.objects.all(),
            'departments': models.Department.objects.all(),
            # permissions
            'has_perm_to_modify': inquiry.has_perm_to_modify(request.user),
            'has_perm_to_manage_status': inquiry.has_perm_to_manage_status(request.user),
        }
        return render(request, self.template_name, context)


class InquiryDelete(LoginRequiredMixin, View):

    def get(self, request, inquiry_id):
        if not models.Inquiry.has_perm_to_modify(request.user):
            raise PermissionDenied
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        inquiry.delete()
        messages.success(request, 'استعلام با موفقیت حذف شد')
        return redirect('public:inquiry__list')


class InquiryUpdate(LoginRequiredMixin, View):

    def post(self, request, inquiry_id):
        if not models.Inquiry.has_perm_to_modify(request.user):
            raise PermissionDenied
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        data = request.POST
        f = forms.InquiryUpdate(data, instance=inquiry)
        if form_validate_err(request, f) is False:
            return redirect(inquiry.get_absolute_url())
        f.save()
        messages.success(request, 'استعلام با موفقیت بروزرسانی شد')
        return redirect(inquiry.get_absolute_url())


class InquiryStatusModify(LoginRequiredMixin, View):

    def post(self, request, inquiry_id):
        if not models.Inquiry.has_perm_to_manage_status(request.user):
            raise PermissionDenied
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        data = request.POST.copy()
        # set additional values
        data['inquiry'] = inquiry
        inquiry_status = getattr(inquiry, 'status', None)
        f = forms.InquiryStatusModify(data, files=request.FILES, instance=inquiry_status)
        if not form_validate_err(request, f):
            return redirect(inquiry.get_absolute_url())
        f.save()
        messages.success(request, 'وضعیت استعلام با موفقیت ثبت و بروزرسانی شد')
        return redirect(inquiry.get_absolute_url())


class InquiryFileAdd(LoginRequiredMixin, View):

    def post(self, request, inquiry_id):
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        data = request.POST.copy()
        user = request.user
        # set additional values
        data['inquiry'] = inquiry
        data['from_department'] = user.department
        data['allocator_user'] = user
        f = forms.InquiryFile(data, request.FILES)
        if not form_validate_err(request, f):
            return redirect(inquiry.get_absolute_url())
        # create and upload files
        files_object = []
        files = request.FILES.getlist('files')
        for file in files:
            files_object.append(models.File(file=file))
        files_object = models.File.objects.bulk_create(files_object)
        inquiry_file = f.save()
        inquiry_file.files.add(*files_object)
        messages.success(request, 'فایل پیوست با ایجاد و اپلود شد')
        return redirect(inquiry.get_absolute_url())


class InquiryFileDelete(LoginRequiredMixin, View):

    def get(self, request, inquiry_id, inquiry_file_id):
        inquiry_file = get_object_or_404(models.InquiryFile, id=inquiry_file_id, inquiry_id=inquiry_id)
        if inquiry_file.from_department != request.user.department:
            raise PermissionDenied
        inquiry_file.delete()
        messages.success(request, 'فایل استعلام با موفقیت حذف شد')
        return redirect(inquiry_file.inquiry.get_absolute_url())


class TaskMasterAdd(LoginRequiredMixin, View):
    template_name = 'public/task_master/add.html'

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def get(self, request):
        return render(request, self.template_name)

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def post(self, request):
        data = request.POST
        f = forms.TaskMasterCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect('public:task_master__add')
        task_master = f.save()
        messages.success(request, 'مشتری با موفقیت ایجاد شد')
        return redirect(task_master.get_absolute_url())


class TaskMasterList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/task_master/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def filter(self, task_masters):
        qs = self.request.GET
        search = qs.get('search', None)
        if search:
            task_masters = task_masters.filter(name__icontains=search)
        return task_masters

    def sort(self, task_masters):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            task_masters = task_masters.order_by('-id')
        elif sort_by == 'oldest':
            task_masters = task_masters.order_by('id')
        elif sort_by == 'most-project':
            task_masters = task_masters.annotate(c=Count('projects')).order_by('-c')

        return task_masters

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def get(self, request):
        task_masters = models.TaskMaster.objects.all()
        task_masters = self.filter(task_masters)
        task_masters = self.sort(task_masters)
        pagination, task_masters = self.pagination(task_masters)
        context = {
            'pagination': pagination,
            'task_masters': task_masters
        }
        return render(request, self.template_name, context)


class TaskMasterDetail(LoginRequiredMixin, View):
    template_name = 'public/task_master/detail.html'

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def get(self, request, task_master_id):
        task_master = get_object_or_404(models.TaskMaster, id=task_master_id)
        context = {
            'task_master': task_master,
            # permissions
            'has_perm_to_modify': task_master.has_perm_to_modify(request.user),
            'has_perm_to_delete': task_master.has_perm_to_delete(request.user),
        }
        return render(request, self.template_name, context)


class TaskMasterDelete(LoginRequiredMixin, View):
    def get(self, request, task_master_id):
        if not models.TaskMaster.has_perm_to_delete(request.user):
            raise PermissionDenied
        task_master = get_object_or_404(models.TaskMaster, id=task_master_id)
        task_master.delete()
        messages.success(request, 'مشتری با موفقیت حذف شد')
        return redirect('public:task_master__list')


class TaskMasterUpdate(LoginRequiredMixin, View):
    def post(self, request, task_master_id):
        if not models.TaskMaster.has_perm_to_modify(request.user):
            raise PermissionDenied
        task_master = get_object_or_404(models.TaskMaster, id=task_master_id)
        f = forms.TaskMasterUpdate(request.POST, instance=task_master)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(task_master.get_absolute_url())
        f.save()
        messages.success(request, 'مشتری با موفقیت بروزرسانی شد')
        return redirect(task_master.get_absolute_url())


class DepartmentAdd(LoginRequiredMixin, View):
    template_name = 'public/department/add.html'

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request):
        return render(request, self.template_name)

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def post(self, request):
        data = request.POST
        f = forms.DepartmentCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('public:department__add')
        f.save()
        messages.success(request, 'واحد با موفقیت ایجاد شد')
        return redirect('public:department__add')


class DepartmentList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/department/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def sort(self, departments):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            departments = departments.order_by('-id')
        elif sort_by == 'oldest':
            departments = departments.order_by('id')
        elif sort_by == 'most-tasks':
            departments = departments.annotate(c=Count('task')).order_by('-c')
        return departments

    def filter(self, departments):
        qs = self.request.GET
        search = qs.get('search', None)
        if search:
            departments = departments.filter(name__icontains=search)
        return departments

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request):
        departments = models.Department.objects.all()
        departments = self.filter(departments)
        departments = self.sort(departments)
        pagination, departments = self.pagination(departments)
        context = {
            'pagination': pagination,
            'departments': departments,
        }
        return render(request, self.template_name, context)


class DepartmentDetail(LoginRequiredMixin, View):
    template_name = 'public/department/detail.html'

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request, department_id):
        department = get_object_or_404(models.Department, id=department_id)
        context = {
            'department': department,
            # permissions
            'has_perm_to_modify': department.has_perm_to_modify(request.user),
            'has_perm_to_delete': department.has_perm_to_delete(request.user),
        }
        return render(request, self.template_name, context)


class DepartmentDelete(LoginRequiredMixin, View):
    template_name = 'public/department/detail.html'

    def get(self, request, department_id):
        if not models.Department.has_perm_to_delete(request.user):
            raise PermissionDenied
        department = get_object_or_404(models.Department, id=department_id)
        department.delete()
        messages.success(request, 'واحد با موفقیت حذف شد')
        return redirect('public:department__list')


class DepartmentUpdate(LoginRequiredMixin, View):
    def post(self, request, department_id):
        if not models.Department.has_perm_to_modify(request.user):
            raise PermissionDenied
        department = get_object_or_404(models.Department, id=department_id)
        f = forms.DepartmentUpdate(request.POST, instance=department)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(department.get_absolute_url())
        f.save()
        messages.success(request, 'واحد با موفقیت بروزرسانی شد')
        return redirect(department.get_absolute_url())


class ProjectFileAdd(LoginRequiredMixin, View):
    template_name = 'public/project_file/add.html'

    def get(self, request):
        context = {
            'projects': models.Project.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST.copy()
        # set additional values
        user = request.user
        data['allocator_user'] = user
        data['from_department'] = user.department
        f = forms.ProjectFileCreate(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('public:project_file__add')
        f.save()
        messages.success(request, 'فایل پروژه با موفقیت ایجاد و اپلود شد')
        return redirect(referer_url or 'public:project_file__add')


class ProjectFileList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/project_file/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def sort(self, project_files):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            project_files = project_files.order_by('-id')
        elif sort_by == 'oldest':
            project_files = project_files.order_by('id')
        return project_files

    def filter(self, project_files):
        qs = self.request.GET
        search = qs.get('search', None)
        if search:
            project_files = project_files.filter(name__icontains=search)
        return project_files

    def get(self, request):
        project_files = models.ProjectFile.objects.all()
        project_files = self.filter(project_files)
        project_files = self.sort(project_files)
        pagination, project_files = self.pagination(project_files)
        context = {
            'pagination': pagination,
            'project_files': project_files,
            'projects': models.Project.objects.all()
        }
        return render(request, self.template_name, context)


class ProjectFileDetail(LoginRequiredMixin, View):
    template_name = 'public/project_file/detail.html'

    def get(self, request, project_file_id):
        project_file = get_object_or_404(models.ProjectFile, id=project_file_id)
        context = {
            'project_file': project_file,
            # permissions
            'has_perm_to_modify': project_file.has_perm_to_modify(request.user)
        }
        return render(request, self.template_name, context)


class ProjectFileDelete(LoginRequiredMixin, View):

    def get(self, request, project_file_id):
        project_file = get_object_or_404(models.ProjectFile, id=project_file_id)
        if not project_file.has_perm_to_modify(request.user):
            raise PermissionDenied
        project_file.delete()
        messages.success(request, 'فایل پروژه با موفقیت حذف شد')
        return redirect('public:project_file__list')
