import jdatetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django_q.models import Schedule
from account.auth.decorators import user_role_required_cbv
from notification.utils import create_notification_by_role
from public.models import Project
from . import forms, models


class Index(LoginRequiredMixin, View):
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


class PaymentAdd(LoginRequiredMixin, View):
    template_name = 'financial/payment/add.html'

    @user_role_required_cbv(['financial_user', 'super_user'])
    def get(self, request):
        context = {
            'payment': models.Payment,
            'projects': Project.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['financial_user', 'super_user'])
    def post(self, request):
        data = request.POST
        f = forms.PaymentCreate(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect('dp_financial:payment__add')
        payment = f.save()
        create_notification_by_role(
            'پرداختی جدید',
            description='ایجاد به صورت خودکار',
            from_department=request.user.department,
            to_users=('financial_user', 'super_user', 'control_project_user'),
            projects=(payment.project,),
            attached_link=payment.get_absolute_url()
        )
        messages.success(request, 'پرداختی با موفقیت ثبت شد')
        return redirect('dp_financial:payment__add')


class PaymentList(LoginRequiredMixin, View):
    template_name = 'financial/payment/list.html'
    pagination_count = 25

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def sort(self, payments):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            payments = payments.order_by('-id')
        elif sort_by == 'oldest':
            payments = payments.order_by('id')
        elif sort_by == 'high-price':
            payments = payments.order_by('-price')
        return payments

    def filter(self, payments):
        qs = self.request.GET
        search = qs.get('search', None)
        project = qs.get('project', 'all')
        type_payment = qs.get('type_payment', 'all')
        type_status_payment = qs.get('type_status_payment', 'all')
        if search:
            payments = payments.filter(tracking_code__icontains=search)
        if (project != 'all') and (project.isdigit()):
            payments = payments.filter(project_id=project)

        if type_status_payment != 'all':
            payments = payments.filter(type_status_payment=type_status_payment)

        if type_payment != 'all':
            payments = payments.filter(type_payment=type_payment)
        return payments

    @user_role_required_cbv(['financial_user', 'super_user', 'control_project_user'])
    def get(self, request):
        payments = models.Payment.objects.all()
        payments = self.filter(payments)
        payments = self.sort(payments)
        pagination, payments = self.pagination(payments)
        context = {
            'pagination': pagination,
            'payments': payments,
            'projects': Project.objects.filter(is_active=True),
            'TYPE_PAYMENT_OPTIONS': models.Payment.TYPE_PAYMENT_OPTIONS,
            'TYPE_STATUS_PAYMENT_OPTIONS': models.Payment.TYPE_STATUS_PAYMENT_OPTIONS,
        }
        return render(request, self.template_name, context)


class PaymentDetail(LoginRequiredMixin, View):
    template_name = 'financial/payment/detail.html'

    @user_role_required_cbv(['financial_user', 'super_user', 'control_project_user'])
    def get(self, request, payment_id):
        payment = get_object_or_404(models.Payment, id=payment_id)
        context = {
            'payment': payment,
            'projects': Project.objects.filter(is_active=True),
            # permissions
            'has_perm_to_modify': models.Payment.has_perm_to_modify(request.user)
        }
        return render(request, self.template_name, context)


class PaymentDelete(LoginRequiredMixin, View):

    def get(self, request, payment_id):
        payment = get_object_or_404(models.Payment, id=payment_id)
        if not payment.has_perm_to_modify(request.user):
            raise PermissionDenied
        payment.delete()
        messages.success(request, 'پرداختی با موفقیت حذف شد')
        return redirect('dp_financial:payment__list')


class PaymentUpdate(LoginRequiredMixin, View):

    def post(self, request, payment_id):
        payment = get_object_or_404(models.Payment, id=payment_id)
        if not payment.has_perm_to_modify(request.user):
            raise PermissionDenied
        data = request.POST
        f = forms.PaymentUpdate(data, files=request.FILES, instance=payment)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(payment.get_absolute_url())
        f.save()
        messages.success(request, 'پرداختی با موفقیت بروزرسانی شد')
        return redirect(payment.get_absolute_url())


class SuretyBondAdd(LoginRequiredMixin, View):
    template_name = 'financial/surety_bond/add.html'

    @user_role_required_cbv(['financial_user', 'super_user'])
    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True, suretybond=None)
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['financial_user', 'super_user'])
    def post(self, request):
        data = request.POST
        f = forms.SuretyBondCreate(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلدهارا به درستی پر نمایید')
            return redirect('dp_financial:surety_bond__add')
        surety_bond = f.save()
        messages.success(request, 'ضمانت نامه با موفقیت ثبت شد')
        return redirect(surety_bond.get_absolute_url())


class SuretyBondList(LoginRequiredMixin, View):
    template_name = 'financial/surety_bond/list.html'
    pagination_count = 25

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def sort(self, surety_bonds):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            surety_bonds = surety_bonds.order_by('-id')
        elif sort_by == 'oldest':
            surety_bonds = surety_bonds.order_by('id')
        return surety_bonds

    def filter(self, surety_bonds):
        qs = self.request.GET
        search = qs.get('search', None)
        project = qs.get('project', 'all')
        status = qs.get('status', 'all')
        if search:
            surety_bonds = surety_bonds.filter(number_id__icontains=search)
        if (project != 'all') and (project.isdigit()):
            surety_bonds = surety_bonds.filter(project_id=project)

        if status != 'all':
            surety_bonds = surety_bonds.filter(status=status)

        return surety_bonds

    @user_role_required_cbv(['financial_user', 'super_user', 'control_project_user'])
    def get(self, request):
        surety_bonds = models.SuretyBond.objects.all()
        surety_bonds = self.filter(surety_bonds)
        surety_bonds = self.sort(surety_bonds)
        pagination, surety_bonds = self.pagination(surety_bonds)
        context = {
            'pagination': pagination,
            'surety_bonds': surety_bonds,
            'projects': Project.objects.filter(is_active=True),
        }
        return render(request, self.template_name, context)


class SuretyBondDetail(LoginRequiredMixin, View):
    template_name = 'financial/surety_bond/detail.html'

    @user_role_required_cbv(['financial_user', 'super_user', 'control_project_user'])
    def get(self, request, surety_bond_id):
        surety_bond = get_object_or_404(models.SuretyBond, id=surety_bond_id)
        context = {
            'surety_bond': surety_bond,
            'projects': Project.objects.filter(is_active=True),
            # permissions
            'has_perm_to_modify': surety_bond.has_perm_to_modify(request.user)
        }
        return render(request, self.template_name, context)


class SuretyBondDelete(LoginRequiredMixin, View):

    def get(self, request, surety_bond_id):
        surety_bond = get_object_or_404(models.SuretyBond, id=surety_bond_id)
        if not surety_bond.has_perm_to_modify(request.user):
            raise PermissionDenied
        surety_bond.delete()
        messages.success(request, 'ضمانت نامه با موفقیت حذف شد')
        return redirect('dp_financial:surety_bond__list')


class SuretyBondUpdate(LoginRequiredMixin, View):

    def post(self, request, surety_bond_id):
        surety_bond = get_object_or_404(models.SuretyBond, id=surety_bond_id)
        if not surety_bond.has_perm_to_modify(request.user):
            raise PermissionDenied
        data = request.POST
        f = forms.SuretyBondUpdate(data, files=request.FILES, instance=surety_bond)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(surety_bond.get_absolute_url())
        surety_bond = f.save()
        messages.success(request, 'ضمانت نامه با موفقیت بروزرسانی شد')
        return redirect(surety_bond.get_absolute_url())


class ReminderAdd(LoginRequiredMixin, View):
    template_name = 'financial/reminder/add.html'

    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True, reminderproject=None)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        f = forms.ReminderTimeProjectCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('dp_financial:reminder__add')
        reminder = f.save()
        t = reminder.time
        time_reminder_utc = jdatetime.date(t.year, t.month, t.day).togregorian()
        Schedule.objects.create(
            name='send_reminder_notify_financial_project',
            func='departments.financial.tasks.send_reminder_notify_financial_project',
            schedule_type=Schedule.ONCE,
            next_run=time_reminder_utc,
            repeats=1,
            kwargs={
                'reminder_id': reminder.id,
                'from_department_id': request.user.department.id
            }
        )
        messages.success(request, 'یادآور با موفقیت ایجاد شد')
        return redirect('dp_financial:reminder__add')


class ReminderList(LoginRequiredMixin, View):
    template_name = 'financial/reminder/list.html'
    pagination_count = 12

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def sort(self, reminders):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            reminders = reminders.order_by('-id')
        elif sort_by == 'oldest':
            reminders = reminders.order_by('id')
        return reminders

    def filter(self, reminders):
        qs = self.request.GET
        search = qs.get('search', None)
        project = qs.get('project', 'all')
        if search:
            reminders = reminders.filter(description__icontains=search)
        if (project != 'all') and (project.isdigit()):
            reminders = reminders.filter(project_id=project)

        return reminders

    @user_role_required_cbv(['financial_user', 'super_user', 'control_project_user'])
    def get(self, request):
        reminders = models.ReminderProject.objects.all()
        reminders = self.filter(reminders)
        reminders = self.sort(reminders)
        pagination, reminders = self.pagination(reminders)
        context = {
            'pagination': pagination,
            'reminders': reminders,
            'projects': Project.objects.filter(is_active=True),
        }
        return render(request, self.template_name, context)


class ReminderDelete(LoginRequiredMixin, View):

    def get(self, request, reminder_id):
        reminder = get_object_or_404(models.ReminderProject, id=reminder_id)
        if not reminder.has_perm_to_modify(request.user):
            raise PermissionDenied
        reminder.delete()
        messages.success(request, 'یادآور با موفقیت حذف شد')
        return redirect('dp_financial:reminder__list')
