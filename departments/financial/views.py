from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic import View
from django_q.models import Schedule
from account.auth.decorators import user_role_required_cbv
from core.utils import form_validate_err
from public.models import Project, TaskMaster
from . import forms


class Index(View):
    template_name = 'financial/index.html'

    @user_role_required_cbv(['financial_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)

        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
            'projects': projects,
            'ongoing_projects': projects.filter(status__in=['checking', 'paused', 'under_construction'])[:4],
        }
        return render(request, self.template_name, context)


# ProjectsList view
class ProjectListView(View):
    template = 'financial/projects_list.html'

    def filter(self, request, projects):
        search = request.GET.get('search')
        task_master = request.GET.get('task_master', None)

        if search:
            projects = projects.filter(name__icontains=search)

        if task_master and task_master.isdigit():
            projects = projects.filter(task_master_id=task_master)

        return projects

    def get(self, request):
        projects = Project.objects.all()
        projects = self.filter(request, projects)  # Filter projects

        context = {
            'projects': projects,
            'task_masters': TaskMaster.objects.all(),
        }

        return render(request, self.template, context)


class Payment(View):

    @user_role_required_cbv(['financial_user'])
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST
        f = forms.PaymentForm(data)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class PrePayment(View):

    @user_role_required_cbv(['financial_user'])
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST

        f = forms.PrePaymentForm(data)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        obj = f.save()

        # Save prepayment for project
        project = obj.project
        project.prepayment_datetime = obj.submited_at
        project.save()

        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class PaymentProject(View):
    template_name = 'financial/project_payments.html'

    @user_role_required_cbv(['financial_user'])
    def get(self, request, project_id):
        project_obj = Project.objects.get(id=project_id)
        context = {
            'project': project_obj
        }
        return render(request, self.template_name, context)


# SaveSuretyBond view
class SaveSuretyBondView(View):
    @user_role_required_cbv(['financial_user'])
    def post(self, request):
        data = request.POST
        project = Project.objects.get(id=data.get('project'))

        if hasattr(project, 'surety_bond'):
            f = forms.SaveSuretyBondForm(data, instance=project.surety_bond, files=request.FILES)
        else:
            f = forms.SaveSuretyBondForm(data, files=request.FILES)

        if form_validate_err(request, f) is False:
            return redirect(reverse('departments.financial:payment_project', args=(project.id,)))
        f.save()

        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(reverse('departments.financial:payment_project', args=(project.id,)))


# Save ReminderTime view
class ReminderTimeView(View):

    def create_schedule_task(self, request, task_name='financial_reminder_task'):
        try:
            task = Schedule.objects.get(name=task_name)
            task.delete()
        except Schedule.DoesNotExist:
            pass

        department = request.user.department
        Schedule.objects.create(
            name=task_name,
            func='core.tasks.send_reminder_notif',
            kwargs={'from_department': department, 'department': department},
            schedule_type=Schedule.DAILY,
        )

    def create_form(self, data, instance=None, attr: str = None):
        if hasattr(instance, attr):
            instance = getattr(instance, attr)
            return forms.SaveReminderTimeForm(data, instance=instance)

        return forms.SaveReminderTimeForm(data)

    @user_role_required_cbv(['financial_user'])
    def post(self, request):
        data = request.POST
        project = Project.objects.get(id=data.get('project'))

        f = self.create_form(data, project, 'surety_bond')
        if form_validate_err(request, f) is False:
            return redirect(reverse('departments.financial:payment_project', args=(project.id,)))
        obj = f.save()

        self.create_schedule_task(request)  # Create schedule reminder

        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(reverse('departments.financial:payment_project', args=(project.id,)))
