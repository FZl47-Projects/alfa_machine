from django.contrib import messages
from django.shortcuts import render, Http404, redirect, HttpResponse, get_object_or_404
from django.views.generic import View
from core.utils import form_validate_err
from public import models, forms
from account.auth.decorators import user_role_required_cbv


class Success(View):
    def get(self, request):
        return HttpResponse('عملیات با موفقیت انجام شد')


class Error(View):
    def get(self, request):
        return HttpResponse('عملیات با خطا مواجه شد')


class Index(View):

    def get(self, request):
        return redirect(request.user.get_absolute_url_dashboard())


class ProjectDetail(View):
    template_name = 'public/project/detail.html'

    def get(self, request, project_id):
        context = {
            'project': models.Project.objects.get(id=project_id)
        }
        return render(request, self.template_name, context)


class Project(View):
    template_name = 'public/project/list.html'

    def get(self, request):
        context = {
            'projects': models.Project.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)


class ProjectFile(View):

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST
        f = forms.ProjectFile(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات مورد نظر با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class TaskOwner(View):
    """
        get tasks who created and crud task with post method
    """

    def get_template_name(self, request):
        task_state = request.GET.get('task_state', None)
        template_name = None
        if task_state == 'progress':
            template_name = 'public/task/progress.html'
        elif task_state == 'queue':
            template_name = 'public/task/queue.html'
        elif task_state == 'need-to-check':
            template_name = 'public/task/need-to-check.html'
        elif task_state == 'finished':
            template_name = 'public/task/finished.html'
        elif task_state == 'department-each':
            template_name = 'public/task/department-each.html'

        if template_name is None:
            raise Http404
        return template_name

    def get(self, request):
        # get task list by type state
        task_state = request.GET.get('task_state', None)
        department = request.user.department
        tasks = models.Task.objects.filter(from_department=department)
        if task_state:
            tasks = tasks.filter(state=task_state)
        context = {
            'tasks': tasks,
            'departments': models.Department.objects.all(),
            'projects': models.Project.objects.filter(is_active=True)
        }
        template_name = self.get_template_name(request)
        return render(request, template_name, context)

    def post(self, request, task_id):
        type_request = request.POST.get('type_request', None)
        referer_url = request.META.get('HTTP_REFERER', None)

        if type_request == 'update':
            data = request.POST
            task_obj = models.Task.objects.get(id=task_id, from_department=request.user.department)
            f = forms.TaskUpdateForm(data, request.FILES, instance=task_obj)
            if form_validate_err(request, f) is False:
                return redirect(referer_url or '/error')
            f.save()
            messages.success(request, 'تسک با موفقیت بروزرسانی شد')
        elif type_request == 'delete':
            models.Task.objects.get(id=task_id).delete()

        return redirect(referer_url or '/success')


class TaskOwnerDepartment(View):
    template_name = 'public/task/department-each.html'

    def get(self, request, department_id):
        department = models.Department.objects.get(id=department_id)
        tasks = models.Task.objects.filter(to_department=department)
        context = {
            'tasks': tasks,
            'department': department,
            'departments': models.Department.objects.all(),
            'projects': models.Project.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)


class Task(View):
    """
         get and create task
    """

    def get(self, request):
        user_department = request.user.department
        context = {
            'department': user_department,
            'task_states': models.Task.STATE_OPTIONS,
            'tasks': models.Task.objects.filter(to_department=user_department, is_active=True)
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
        f.save()
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

    def get(self, request):
        context = {
            'inquiries': models.Inquiry.objects.filter(status=None)
        }
        return render(request, 'public/inquiry/list.html', context)

    @user_role_required_cbv(['super_user', 'commerce_user'])
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST.copy()
        # set default values
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

    @user_role_required_cbv(['commerce_user'])
    def get(self, request):
        context = {
            'inquiries': models.Inquiry.objects.all(),
            'inquiries_accepted': models.Inquiry.objects.filter(status__status='accepted'),
            'inquiries_rejected': models.Inquiry.objects.filter(status__status='rejected'),
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
        return redirect ('departments.general:departments_list')

