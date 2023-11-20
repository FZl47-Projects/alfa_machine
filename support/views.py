from django.contrib import messages
from django.views.generic import View
from django.shortcuts import redirect, render
from account.auth.decorators import user_role_required_cbv
from core.utils import form_validate_err
from public.models import Department, Project
from django.shortcuts import get_object_or_404
from . import forms, models


class Ticket(View):
    template_name = 'support/list.html'

    def get(self, request):
        context = {
            'tickets': request.user.get_tickets()
        }
        return render(request, self.template_name, context)


# DeleteTicket view
class DeleteTicketView(View):
    template_name = 'support/list.html'

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)

        ticket_id = request.POST.get('ticket_id')
        ticket = get_object_or_404(models.TicketDepartment, id=ticket_id)

        ticket.is_open = False
        ticket.save()

        messages.success(request, 'تیکت با موفقیت حذف گردید.')
        return redirect(referer_url or '/success')


class TicketDepartment(View):

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

        f = forms.TicketDepartmentForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()

        messages.success(request, 'عملیات مورد نظر با موفقیت انجام شد')

        return redirect(referer_url or '/success')


class ReportList(View):
    template_name = 'support/report/list.html'

    @user_role_required_cbv(['control_project_user', 'super_user'])
    def get(self, request):
        context = {
            'reports': models.Report.objects.all()
        }
        return render(request, self.template_name, context)


class ReportDepartmentCreate(View):

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

        f = forms.ReportDepartmentForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()

        messages.success(request, 'عملیات مورد نظر با موفقیت انجام شد')

        return redirect(referer_url or '/success')


class ReportDepartmentList(View):
    template_name = 'support/report/department/list.html'

    def get(self, request):
        context = {
            'reports': request.user.get_reports()
        }
        return render(request, self.template_name, context)
