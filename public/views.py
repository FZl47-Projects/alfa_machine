from django.contrib import messages
from django.shortcuts import render, Http404, redirect, HttpResponse, get_object_or_404
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import form_validate_err
from public import models, forms
from account.auth.decorators import user_role_required_cbv
from notification.models import NotificationDepartment


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

    def get(self, request, project_id):
        context = {
            'has_perm_to_modify': models.Project.has_perm_to_modify(request.user),
            'project': models.Project.objects.get(id=project_id),
            'task_masters': models.TaskMaster.objects.all()
        }
        return render(request, self.template_name, context)


class Project(View):
    template_name = 'public/project/list.html'

    def filter(self, request, projects):
        search = request.GET.get('search')
        task_master = request.GET.get('task_master', None)
        if search:
            projects = projects.filter(name__icontains=search)
        if task_master and task_master.isdigit():
            projects = projects.filter(task_master_id=task_master)
        return projects

    def get(self, request):
        # Get project status and filter by them (if exists)
        project_status = request.GET.get('status')

        if not project_status:
            projects = models.Project.objects.filter(is_active=True)
        elif project_status == 'other':
            projects = models.Project.objects.filter(is_active=True,
                                                     status__in=['checking', 'paused', 'under_construction'])
        else:
            projects = models.Project.objects.filter(is_active=True, status=project_status)

        projects = self.filter(request, projects)

        context = {
            'projects': projects,
            'task_masters': models.TaskMaster.objects.all()
        }
        return render(request, self.template_name, context)


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

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST.copy()
        # set additional values
        data['from_department'] = request.user.department
        f = forms.ProjectFile(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات مورد نظر با موفقیت انجام شد')
        return redirect(referer_url or '/success')


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

        if request.user.role == 'super_user':
            tasks = models.Task.objects.filter(is_active=True)
        else:
            tasks = models.Task.objects.filter(from_department=department)

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
                title='اعلان بروزرسانی تسک',
                description=f'بروزرسانی برای تسک: "{task.name}"'
            )
            notif.departments.set([task.to_department])
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

        notif = NotificationDepartment.objects.create(
            from_department=request.user.department,
            title='اطلاعیه تسک جدید',
            description=f'عنوان تسک: "{task.name}"'
        )
        notif.departments.set([task.to_department])
        notif.projects.set([task.project])

        messages.success(request, 'عملیات مورد نظر با موفقیت ایجاد شد')

        return redirect(referer_url or '/success')


class TaskRemind(LoginRequiredMixin, View):

    def post(self, request, task_id):
        referer_url = request.META.get('HTTP_REFERER', None)

        user = request.user
        department = user.department
        task = get_object_or_404(models.Task, id=task_id)

        notif = NotificationDepartment.objects.create(
            from_department=department,
            title='یاداوری انجام تسک',
            description=f"""
                یاداوری جهت انجام تسک ({task.name})
            """
        )
        notif.departments.set([task.to_department])
        notif.projects.set([task.project])

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

    def search(self, request, inquiries):
        search = request.GET.get('search', None)
        if not search:
            return inquiries
        if search.isdigit():
            lookup = Q(number_id=search)
            inquiries = inquiries.filter(lookup)
        else:
            lookup = Q(title__icontains=search) | Q(from_department__name__icontains=search) | Q(state=search) | Q(
                sender__icontains=search)
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
        inquiries = models.Inquiry.objects.all()
        inquiries = self.search(request, inquiries)
        inquiries = self.sort(request, inquiries)
        context = {
            'inquiries': inquiries,
            'departments': models.Department.objects.all()
        }
        return render(request, 'public/inquiry/list.html', context)

    @user_role_required_cbv(['super_user', 'commerce_user'])
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST.copy()
        # set additional values
        data['from_department'] = request.user.department
        f = forms.InquiryForm(data)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات با موفقیت ثبت شد')
        return redirect(referer_url or '/success')


class InquiryDetail(View):

    @user_role_required_cbv(['super_user', 'commerce_user'])
    def post(self, request, inquiry_id):
        referer_url = request.META.get('HTTP_REFERER', None)
        inquiry_obj = models.Inquiry.objects.get(id=inquiry_id)
        type_request = request.POST.get('type_request', None)
        if type_request == 'delete':
            inquiry_obj.delete()
            messages.success(request, 'عملیات با موفقیت ثبت شد')
            return redirect(referer_url or '/success')
        elif type_request == 'update':
            data = request.POST
            f = forms.InquiryUpdateForm(data, instance=inquiry_obj)
            if form_validate_err(request, f) is False:
                return redirect(referer_url or '/error')
            f.save()
            messages.success(request, 'عملیات با موفقیت ثبت شد')
            return redirect(referer_url or '/success')


class InquiryOwner(View):
    template_name = 'public/inquiry/owner/list.html'

    def search(self, request, inquiries):
        search = request.GET.get('search', None)
        if not search:
            return inquiries
        if search.isdigit():
            lookup = Q(number_id=search)
            inquiries = inquiries.filter(lookup)
        else:
            lookup = Q(title__icontains=search) | Q(from_department__name__icontains=search) | Q(state=search) | Q(
                sender__icontains=search)
            inquiries = inquiries.filter(lookup)
        return inquiries

    def sort(self, request, inquiries):
        sort_by = request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            inquiries = inquiries.order_by('-id')
        elif sort_by == 'oldest':
            inquiries = inquiries.order_by('id')
        return inquiries

    @user_role_required_cbv(['commerce_user'])
    def get(self, request):
        inquiries = models.Inquiry.objects.all()
        inquiries = self.search(request, inquiries)
        inquiries = self.sort(request, inquiries)
        context = {
            'inquiries': inquiries,
            'inquiries_accepted': models.Inquiry.objects.filter(status__status='accepted'),
            'inquiries_rejected': models.Inquiry.objects.filter(status__status='rejected'),
            'departments': models.Department.objects.all()
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
        data = request.POST

        f = forms.ProjectAdd(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('public:project_add')
        f.save()

        messages.success(request, 'پروژه با موفقیت ایجاد شد')
        return redirect('public:project_add')
