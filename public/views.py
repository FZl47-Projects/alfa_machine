from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from account.auth.decorators import user_role_required_cbv
from notification.models import NotificationDepartment
from notification.utils import create_notification
from core.utils import form_validate_err
from public import models, forms


class Success(View):
    def get(self, request):
        return HttpResponse('عملیات با موفقیت انجام شد')


class Error(View):
    def get(self, request):
        return HttpResponse('عملیات با خطا مواجه شد')


class Index(View):
    def get(self, request):
        return redirect(request.user.get_absolute_url_dashboard())


# TaskMaster list/add view
class TaskMasterView(View):
    template = 'public/task_master/list.html'

    def get(self, request):
        task_masters = models.TaskMaster.objects.all()
        contexts = {'task_masters': task_masters}

        return render(request, self.template, contexts)

    def post(self, request):
        data = request.POST

        f = forms.TaskMasterAddForm(data=data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect('public:task_master')
        f.save()

        messages.success(request, 'پروژه با موفقیت بروزرسانی شد')
        return redirect('public:task_master')


class ProjectDetail(View):
    template_name = 'public/project/detail.html'

    def filter(self, request, tasks):
        search = request.GET.get('task_q', None)

        if search:
            tasks = tasks.filter(Q(name__icontains=search) | Q(from_department__name__icontains=search))

        return tasks

    def get(self, request, project_id):
        tasks = models.Task.objects.filter(project_id=project_id)
        tasks = self.filter(request, tasks)

        context = {
            'has_perm_to_modify': models.Project.has_perm_to_modify(request.user),
            'project': models.Project.objects.get(id=project_id),
            'project_tasks': tasks,
            'task_masters': models.TaskMaster.objects.all()
        }
        return render(request, self.template_name, context)


class Project(View):
    template_name = 'public/project/list.html'

    def filter(self, request, projects):
        search = request.GET.get('search', None)
        task_master = request.GET.get('task_master', None)
        project_status = request.GET.get('project_status', None)
        filter_by_date = request.GET.get('filter_by_date', None)

        if search:
            projects = projects.filter(name__icontains=search)
        if task_master and task_master.isdigit():
            projects = projects.filter(task_master_id=task_master)
        if project_status:
            projects = projects.filter(status=project_status)

        if filter_by_date:
            # filter by start and end date project
            time_start_gt = request.GET.get('time_start_gt', None)
            time_start_lt = request.GET.get('time_start_lt', None)
            time_end_gt = request.GET.get('time_end_gt', None)
            time_end_lt = request.GET.get('time_end_lt', None)

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
        # Get project status and filter by them (if exists)
        projects = models.Project.objects.filter(is_active=True)

        projects = self.filter(request, projects)

        context = {
            'projects': projects,
            'task_masters': models.TaskMaster.objects.all()
        }
        return render(request, self.template_name, context)


class ProjectAdd(View):

    @user_role_required_cbv(['super_user', 'commerce_user', 'control_project_user'])
    def get(self, request):
        context = {}

        task_masters = models.TaskMaster.objects.all()
        context['task_masters'] = task_masters
        inquiry_id = request.GET.get('inquiry-id', None)
        if inquiry_id:
            context['inquiry'] = models.Inquiry.objects.get(id=inquiry_id, project=None)

        return render(request, 'public/project/add.html', context)

    @user_role_required_cbv(['super_user', 'commerce_user', 'control_project_user'])
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST

        f = forms.ProjectAdd(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            # redirect to referer url or project add url
            if referer_url:
                return redirect(referer_url)
            return redirect('public:project_add')
        f.save()

        messages.success(request, 'پروژه با موفقیت ایجاد شد')
        # redirect to referer url or project add url
        if referer_url:
            return redirect(referer_url)
        return redirect('public:project_add')


class ProjectUpdate(LoginRequiredMixin, View):

    def post(self, request, project_id):
        if not models.Project.has_perm_to_modify(request.user):
            raise PermissionDenied

        project = models.Project.objects.get(id=project_id)

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

        project = models.Project.objects.get(id=project_id)
        project.delete()

        messages.success(request, 'پروژه با موفقیت حذف شد')
        return redirect('public:project')


class ProjectFile(LoginRequiredMixin, View):

    def search(self, request, items):
        search = request.GET.get('search', None)
        if not search:
            return items
        if search.isdigit():
            lookup = Q(code=search)
            items = items.filter(lookup)
        else:
            lookup = Q(name__icontains=search) | Q(size=search) | Q(receiver__icontains=search)
            items = items.filter(lookup)
        return items

    def sort(self, request, items):
        sort_by = request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            items = items.order_by('-id')
        elif sort_by == 'oldest':
            items = items.order_by('id')
        return items

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user', 'control_quality_user',
                             'technical_user', 'production_user'])
    def get(self, request):
        context = {
            'projects': models.Project.objects.filter(is_active=True)
        }
        return render(request, 'public/project/file/list.html', context)

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST.copy()
        # set additional values
        data['from_department'] = request.user.department

        f = forms.ProjectFile(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        obj = f.save()

        # Create notification for each department
        notif_title = 'اعلان آپلود فایل پروژه'
        notif_description = f'فایل جدید برای پروژه ({obj.project.name})'
        create_notification(from_department=obj.from_department, title=notif_title, description=notif_description, projects=obj.project, all_departments=True)

        messages.success(request, 'عملیات مورد نظر با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class ProjectDetailFileList(LoginRequiredMixin, View):

    def search(self, request, items):
        search = request.GET.get('search', None)
        if not search:
            return items
        items = items.filter(name__icontains=search)
        return items

    def sort(self, request, items):
        sort_by = request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            items = items.order_by('-id')
        elif sort_by == 'oldest':
            items = items.order_by('id')
        return items

    def filter(self, request, items):
        # search
        items = self.search(request, items)
        # filter
        filter_by = request.GET.get('filter_by')
        if filter_by and filter_by.isdigit():
            items = items.filter(from_department__id=filter_by)
        # sort
        items = self.sort(request, items)
        return items

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user', 'control_quality_user',
                             'technical_user', 'production_user'])
    def get(self, request, project_id):
        project = models.Project.objects.get(id=project_id, is_active=True)
        files = project.get_files()
        # search & filter
        files = self.filter(request, files)
        context = {
            'files': files,
            'project': project,
            'departments': models.Department.objects.all()
        }
        return render(request, 'public/project/file/detail.html', context)


class TaskOwner(LoginRequiredMixin, View):
    """
        get tasks who created and crud task with post method
    """

    def search(self, request, tasks):
        search = request.GET.get('search', None)
        if not search:
            return tasks
        lookup = Q(name__icontains=search) | Q(from_department__name__icontains=search)
        tasks = tasks.filter(lookup)
        return tasks

    def sort(self, request, tasks):
        sort_by = request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            tasks = tasks.order_by('-id')
        elif sort_by == 'oldest':
            tasks = tasks.order_by('id')
        return tasks

    def get(self, request):
        # get task list by type state
        task_state = request.GET.get('task_state', None)
        department = request.user.department

        if request.user.role in ('super_user',):
            tasks = models.Task.objects.filter(is_active=True)
        else:
            tasks = models.Task.objects.filter(is_active=True, from_department=department)

        if task_state:
            tasks = tasks.filter(state=task_state)

        tasks = self.search(request, tasks)
        tasks = self.sort(request, tasks)

        context = {
            'tasks': tasks,
            'departments': models.Department.objects.all(),
            'projects': models.Project.objects.filter(is_active=True)
        }

        return render(request, 'public/task/list-state.html', context)

    def post(self, request, task_id):
        type_request = request.POST.get('type_request', None)
        referer_url = request.META.get('HTTP_REFERER', None)

        if type_request == 'update':
            data = request.POST
            task_obj = models.Task.objects.get(id=task_id, from_department=request.user.department)

            f = forms.TaskUpdateForm(data, request.FILES, instance=task_obj)
            if form_validate_err(request, f) is False:
                return redirect(referer_url or '/error')
            task = f.save()

            notif = NotificationDepartment.objects.create(
                from_department=request.user.department,
                department=task.to_department,
                title='اعلان بروزرسانی تسک',
                description=f'بروزرسانی برای تسک: "{task.name}"'
            )
            notif.projects.set([task.project])

            messages.success(request, 'تسک با موفقیت بروزرسانی شد')
        elif type_request == 'delete':
            models.Task.objects.get(id=task_id).delete()

        return redirect(referer_url or '/success')


class TaskOwnerDepartment(View):
    template_name = 'public/task/department-each.html'

    def search(self, request, tasks):
        search = request.GET.get('search', None)
        if not search:
            return tasks
        lookup = Q(name__icontains=search) | Q(from_department__name__icontains=search)
        tasks = tasks.filter(lookup)
        return tasks

    def sort(self, request, tasks):
        sort_by = request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            tasks = tasks.order_by('-id')
        elif sort_by == 'oldest':
            tasks = tasks.order_by('id')
        return tasks

    def get(self, request, department_id):
        department = models.Department.objects.get(id=department_id)
        tasks = models.Task.objects.filter(to_department=department)

        tasks = self.search(request, tasks)
        tasks = self.sort(request, tasks)

        context = {
            'tasks': tasks,
            'department': department,
            'departments': models.Department.objects.all(),
            'projects': models.Project.objects.filter(is_active=True)
        }

        return render(request, self.template_name, context)


class Task(View):
    """ get and create task """

    def search(self, request, tasks):
        search = request.GET.get('search', None)
        if not search:
            return tasks
        lookup = Q(name__icontains=search) | Q(from_department__name__icontains=search)
        tasks = tasks.filter(lookup)
        return tasks

    def sort(self, request, tasks):
        sort_by = request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            tasks = tasks.order_by('-id')
        elif sort_by == 'oldest':
            tasks = tasks.order_by('id')
        return tasks

    def get(self, request):
        user_department = request.user.department
        tasks = models.Task.objects.filter(to_department=user_department, is_active=True)
        tasks = self.search(request, tasks)
        tasks = self.sort(request, tasks)
        context = {
            'department': user_department,
            'task_states': models.Task.STATE_OPTIONS,
            'tasks': tasks
        }
        return render(request, 'public/task/list.html', context)

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST.copy()

        # set default values
        data['allocator_user'] = request.user
        data['from_department'] = request.user.department
        data['state'] = 'queue'

        f = forms.TaskCreateForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        task = f.save()

        # Create notification for department
        notif_title = 'اطلاعیه تسک جدید'
        notif_description = f'عنوان تسک: "{task.name}"'
        create_notification(
            from_department=request.user.department,
            title=notif_title, description=notif_description,
            projects=task.project, departments=[task.to_department]
        )

        messages.success(request, 'عملیات مورد نظر با موفقیت ایجاد شد')

        return redirect(referer_url or '/success')


class TaskRemind(LoginRequiredMixin, View):

    def post(self, request, task_id):
        referer_url = request.META.get('HTTP_REFERER', None)

        user = request.user
        department = user.department
        task = get_object_or_404(models.Task, id=task_id)

        # Create notification for department
        notif_title = 'یادآوری انجام تسک'
        notif_description = f'یادآوری جهت انجام تسک ({task.name})'
        create_notification(
            from_department=department,
            title=notif_title, description=notif_description,
            projects=task.project, departments=[task.to_department]
        )

        messages.success(request, 'عملیات مورد نظر با موفقیت ایجاد شد')

        return redirect(referer_url or '/success')


class TaskListStateUpdate(View):

    # @user_role_required_cbv(['super_user', 'control_project_user'])
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST
        request_department = request.user.department
        tasks = models.Task.objects.filter(to_department=request_department)
        for task in tasks:
            task_data_state = data.get(f'task-state-{task.id}', None)
            if task_data_state:
                f = forms.TaskStateUpdate(data={'state': task_data_state})
                if form_validate_err(request, f) is False:
                    return redirect(referer_url or '/error')
                task.state = task_data_state
                task.save()
        messages.success(request, 'عملیات مورد نظر با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class Inquiry(View):

    def filter(self, request, inquiries):
        archived = request.GET.get('archived', False)
        task_master = request.GET.get('task_master', None)
        filter_by_state = request.GET.get('filter_by_state', None)

        if archived:
            inquiries = inquiries.filter(Q(state='canceled') | Q(time_deadline_response__lt=timezone.now()))
        else:
            # inquiries = inquiries.filter(~Q(state='canceled') & Q(time_deadline_response__gt=timezone.now()))
            pass

        if task_master and task_master.isdigit():
            inquiries = inquiries.filter(sender_id=task_master)

        if filter_by_state:
            inquiries = inquiries.filter(state=filter_by_state)

        return inquiries

    def search(self, request, inquiries):
        search = request.GET.get('search', None)

        if not search:
            return inquiries
        if search.isdigit():
            lookup = Q(number_id=search)
            inquiries = inquiries.filter(lookup)
        else:
            lookup = Q(title__icontains=search) | Q(from_department__name__icontains=search) | Q(state=search) | Q(
                sender__title__icontains=search)
            inquiries = inquiries.filter(lookup)
        return inquiries

    def sort(self, request, inquiries):
        sort_by = request.GET.get('sort_by', 'latest')

        if sort_by == 'latest':
            inquiries = inquiries.order_by('-id')
        elif sort_by == 'oldest':
            inquiries = inquiries.order_by('id')
        return inquiries

    def get(self, request):
        if request.user.role == 'super_user':
            inquiries = models.Inquiry.objects.all()
        else:
            inquiries = models.Inquiry.objects.exclude(status=None)

        inquiries = self.search(request, inquiries)
        inquiries = self.filter(request, inquiries)
        inquiries = self.sort(request, inquiries)

        context = {
            'inquiries': inquiries,
            'departments': models.Department.objects.all(),
            'taskmasters': models.TaskMaster.objects.all(),
        }

        return render(request, 'public/inquiry/list.html', context)

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user'])
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST.copy()

        # set additional values
        data['from_department'] = request.user.department

        f = forms.InquiryForm(data)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()

        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class InquiryDetail(View):

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user'])
    def post(self, request, inquiry_id):
        referer_url = request.META.get('HTTP_REFERER', None)
        inquiry_obj = models.Inquiry.objects.get(id=inquiry_id)
        type_request = request.POST.get('type_request', None)

        if type_request == 'delete':
            inquiry_obj.delete()
        elif type_request == 'update':
            data = request.POST

            f = forms.InquiryUpdateForm(data, instance=inquiry_obj)
            if form_validate_err(request, f) is False:
                return redirect(referer_url or '/error')
            f.save()

        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class InquiryOwner(View):
    template_name = 'public/inquiry/owner/list.html'

    def filter(self, request, inquiries):
        task_master = request.GET.get('task_master', None)
        filter_by_state = request.GET.get('filter_by_state', None)

        if task_master and task_master.isdigit():
            inquiries = inquiries.filter(sender_id=task_master)

        if filter_by_state:
            inquiries = inquiries.filter(state=filter_by_state)

        return inquiries

    def search(self, request, inquiries):
        search = request.GET.get('search', None)

        if not search:
            return inquiries
        if search.isdigit():
            lookup = Q(number_id=search)
            inquiries = inquiries.filter(lookup)
        else:
            lookup = Q(title__icontains=search) | Q(from_department__name__icontains=search) | Q(state=search) | Q(
                sender__title__icontains=search)
            inquiries = inquiries.filter(lookup)
        return inquiries

    def sort(self, request, inquiries):
        sort_by = request.GET.get('sort_by', 'latest')

        if sort_by == 'latest':
            inquiries = inquiries.order_by('-id')
        elif sort_by == 'oldest':
            inquiries = inquiries.order_by('id')
        return inquiries

    @user_role_required_cbv(['commerce_user', 'procurement_commerce_user'])
    def get(self, request):
        inquiries = models.Inquiry.objects.all()

        inquiries = self.search(request, inquiries)
        inquiries = self.filter(request, inquiries)
        inquiries = self.sort(request, inquiries)

        context = {
            'inquiries': inquiries,
            'inquiries_accepted': models.Inquiry.objects.filter(status__status='accepted'),
            'inquiries_rejected': models.Inquiry.objects.filter(status__status='rejected'),
            'departments': models.Department.objects.all(),
            'taskmasters': models.TaskMaster.objects.all(),
        }
        return render(request, self.template_name, context)


class InquiryStatus(View):

    @user_role_required_cbv(['super_user'])
    def post(self, request, inquiry_id):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST.copy()
        # set default values
        data['inquiry'] = inquiry_id
        f = forms.InquiryStatusForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات با موفقیت ثبت شد')
        return redirect(referer_url or '/success')


class InquiryFile(View):

    def post(self, request, inquiry_id):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST.copy()
        # set additional values
        data['inquiry'] = inquiry_id
        data['from_department'] = request.user.department
        f = forms.InquiryFileForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات با موفقیت ثبت شد')
        return redirect(referer_url or '/success')


class DepartmentDetail(View):
    template_name = 'public/department/department_detail.html'

    @user_role_required_cbv(['super_user'])
    def get(self, request, department_id):
        department = get_object_or_404(models.Department, id=department_id)
        context = {
            'department': department,
            'tasks': models.Task.objects.filter(to_department=department),
        }
        return render(request, self.template_name, context)

    def post(self, request, department_id):
        post = request.POST
        department = models.Department.objects.get(id=department_id)
        department.name = post.get('name', None)
        department.save()
        return redirect('departments.general:departments_list')
