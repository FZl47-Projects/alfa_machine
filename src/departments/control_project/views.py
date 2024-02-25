from django.shortcuts import render
from django.views.generic import View
from public.models import Project, Department, TaskMaster, Inquiry
from account.auth.decorators import user_role_required_cbv


class Index(View):
    template_name = 'control_project/index.html'

    @user_role_required_cbv(['control_project_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)
        context = {
            'task_masters': TaskMaster.objects.all(),
            'inquiries': Inquiry.objects.all(),
            'departments': Department.objects.all(),
            'projects': projects,
        }
        return render(request, self.template_name, context)
