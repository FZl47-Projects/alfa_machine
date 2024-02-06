from django.shortcuts import render
from django.views.generic import View
from public.models import Project, TaskMaster, Inquiry
from account.auth.decorators import user_role_required_cbv


class CommerceIndex(View):
    template_name = 'commerce/index.html'

    @user_role_required_cbv(['commerce_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)
        context = {
            'task_masters': TaskMaster.objects.all(),
            'inquiries': Inquiry.objects.all(),
            'projects': projects,
        }
        return render(request, self.template_name, context)


class ProcurementCommerceIndex(View):
    template = 'commerce/procurement_index.html'

    @user_role_required_cbv(['procurement_commerce_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)
        context = {
            'task_masters': TaskMaster.objects.all(),
            'inquiries': Inquiry.objects.all(),
            'projects': projects,
        }
        return render(request, self.template, context)
