from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from public.models import Department, Project
from account.auth.decorators import user_role_required_cbv
from . import forms, models


class TicketAdd(LoginRequiredMixin, View):
    template_name = 'support/ticket/add.html'

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True),
            'departments': Department.objects.all()
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def post(self, request):
        data = request.POST.copy()
        # set additional values
        user = request.user
        data['from_department'] = user.department
        f = forms.TicketDepartmentCreate(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect('support:ticket__add')
        ticket = f.save(commit=False)
        projects = data.getlist('projects')
        if 'other' in projects:
            ticket.projects_type = 'other'
            ticket.save()
        else:
            ticket.projects_type = 'selected'
            ticket.save()
            ticket.projects.add(*projects)
        ticket.to_departments.add(*data.getlist('to_departments'))
        messages.success(request, 'گزارش با موفقیت ایجاد شد')
        return redirect('support:ticket__add')


class TicketList(LoginRequiredMixin, View):
    USER_ACCESS_TO_ALL = ('super_user', 'control_project_user')
    pagination_count = 25
    template_name = 'support/ticket/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def get_tickets(self):
        """
            get tickets by user department
        """
        tickets = models.TicketDepartment.objects.all()
        user = self.request.user
        if user.role in self.USER_ACCESS_TO_ALL:
            return tickets
        tickets = tickets.filter(to_departments__in=[user.department])
        return tickets

    def sort(self, tickets):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            tickets = tickets.order_by('-id')
        elif sort_by == 'oldest':
            tickets = tickets.order_by('id')
        return tickets

    def filter(self, tickets):
        qs = self.request.GET
        search = qs.get('search', None)
        projects = qs.get('projects', 'all')
        to_departments = qs.get('to_departments', 'all')
        status = qs.get('status', 'all')

        if search:
            tickets = tickets.filter(title__icontains=search)

        if projects == 'other':
            tickets = tickets.filter(projects_type='other')
        else:
            if (projects != 'all') and (projects.isdigit()):
                tickets = tickets.filter(projects__in=[projects])

        if (to_departments != 'all') and (to_departments.isdigit()):
            tickets = tickets.filter(to_departments__in=[to_departments])

        if status != 'all':
            if status == 'open':
                tickets = tickets.filter(is_open=True)
            else:
                tickets = tickets.filter(is_open=False)

        return tickets

    def get(self, request):
        tickets = self.get_tickets()
        tickets = self.filter(tickets)
        tickets = self.sort(tickets)
        pagination, tickets = self.pagination(tickets)
        context = {
            'pagination': pagination,
            'tickets': tickets,
            'projects': models.Project.objects.filter(is_active=True),
            'departments': models.Department.objects.all(),
        }
        return render(request, self.template_name, context)


class TicketDetail(LoginRequiredMixin, View):
    template_name = 'support/ticket/detail.html'

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.TicketDepartment, id=ticket_id)
        context = {
            'ticket': ticket,
            # permissions
            'has_perm_to_modify': ticket.has_perm_to_modify(request.user)
        }
        return render(request, self.template_name, context)


class TicketDelete(LoginRequiredMixin, View):

    def get(self, request, ticket_id):
        ticket = get_object_or_404(models.TicketDepartment, id=ticket_id)
        if not ticket.has_perm_to_modify(request.user):
            raise PermissionDenied
        ticket.delete()
        messages.success(request, 'گزارش با موفقیت حذف شد')
        return redirect('support:ticket__list')


class TicketUpdate(LoginRequiredMixin, View):

    def post(self, request, ticket_id):
        ticket = get_object_or_404(models.TicketDepartment, id=ticket_id)
        if not ticket.has_perm_to_modify(request.user):
            raise PermissionDenied
        f = forms.TicketDepartmentUpdate(request.POST, files=request.FILES, instance=ticket)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(ticket.get_absolute_url())
        f.save()
        messages.success(request, 'گزارش با موفقیت بروزرسانی شد')
        return redirect(ticket.get_absolute_url())
