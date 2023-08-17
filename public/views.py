from django.contrib import messages
from django.shortcuts import render, Http404, redirect
from django.views.generic import View
from core.utils import form_validate_err
from public import models, forms


class ProjectDetail(View):
    template_name = 'public/project/detail.html'

    def get(self, request, project_id):
        context = {
            'project': models.Project.objects.get(id=project_id)
        }
        return render(request,self.template_name,context)


class Project(View):
    template_name = 'public/project/list.html'

    def get(self, request):
        context = {
            'projects': models.Project.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)


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


class TaskDepartment(View):
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


class TaskDetail(View):

    def get(self, request, task_id):
        pass
