from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from core.utils import form_validate_err
from public.models import Project, Department
from .models import NotificationDepartment
from . import forms


class NotificationDepartmentList(View):
    template_name = 'notification/list.html'

    def get(self, request):
        user_department = request.user.department
        notifications = NotificationDepartment.objects.filter(departments__in=[user_department], is_showing=True)
        context = {
            'notifications': notifications
        }
        return render(request, self.template_name, context)

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)

        data = request.POST.copy()

        # Get selected departments & projects
        department_selection = data.get('select_department_ticket', 'all')
        project_selection = data.get('select_project_ticket', 'all')

        # Set default values
        is_all_departments = True if department_selection == 'all' else False
        is_all_projects = True if project_selection == 'all' else False

        if is_all_departments is False:
            departments = data.getlist('departments', [])
        else:
            departments = list(Department.objects.all().values_list('id', flat=True))

        if project_selection == 'null':
            projects = []
        elif is_all_projects is False:
            projects = data.getlist('projects', [])
        else:
            projects = list(Project.objects.filter(is_active=True).values_list('id', flat=True))

        data['from_department'] = request.user.department
        data['is_all_departments'] = is_all_departments
        data['is_all_projects'] = is_all_projects
        data['project_selection'] = project_selection
        data.setlist('projects', projects)
        data.setlist('departments', departments)

        f = forms.NotificationDepartmentForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()

        messages.success(request, 'عملیات مورد نظر با موفقیت انجام شد')

        return redirect(referer_url or '/success')


# DeleteNotificationDepartment view
class DeleteNotificationView(LoginRequiredMixin, View):
    template = 'notification/list.html'

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)

        notif_id = request.POST.get('notif_id')
        notification = get_object_or_404(NotificationDepartment, id=notif_id)

        notification.is_showing = False
        notification.save()

        messages.success(request, 'اعلان با موفقیت حذف گردید.')

        return redirect(referer_url or '/success')
