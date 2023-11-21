from django.shortcuts import render
from django.views.generic import View
from public.models import Project, Department
from account.auth.decorators import user_role_required_cbv


class CommerceIndex(View):
    template_name = 'commerce/index.html'

    @user_role_required_cbv(['commerce_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)

        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
            'projects': projects,
            'ongoing_projects': projects.filter(status__in=['checking', 'paused', 'under_construction'])[:4],
            'departments': Department.objects.all(),
        }
        return render(request, self.template_name, context)


# ProcurementCommerceIndex view
class ProcurementCommerceIndex(View):
    template = 'commerce/procurement_index.html'

    @user_role_required_cbv(['procurement_commerce_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)

        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
            'projects': projects,
            'ongoing_projects': projects.filter(status__in=['checking', 'paused', 'under_construction'])[:4],
            'departments': Department.objects.all(),
        }
        return render(request, self.template, context)
