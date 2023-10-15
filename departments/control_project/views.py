from django.shortcuts import render
from django.views.generic import View
from public.models import Project, Department, Task
from account.auth.decorators import user_role_required_cbv


class Index(View):
    template_name = 'control_project/index.html'

    @user_role_required_cbv(['control_project_user'])
    def get(self, request):
        user = request.user
        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
            'projects': Project.objects.filter(is_active=True),
            'departments': Department.objects.all(),
            'tasks': {
                'progress': Task.objects.filter(state='progress', to_department=user.department).count(),
                'queue': Task.objects.filter(state='queue', to_department=user.department).count(),
                'finished': Task.objects.filter(state='finished', to_department=user.department).count(),
                'need_to_check': Task.objects.filter(state='need-to-check', to_department=user.department).count(),
            }
        }
        return render(request, self.template_name, context)
