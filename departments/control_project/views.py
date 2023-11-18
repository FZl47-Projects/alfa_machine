from django.shortcuts import render
from django.views.generic import View
from public.models import Project, Department, Task
from account.auth.decorators import user_role_required_cbv


class Index(View):
    template_name = 'control_project/index.html'

    @user_role_required_cbv(['control_project_user'])
    def get(self, request):
        user = request.user
        department = user.department
        context = {
            'tickets': user.get_tickets(),
            'notifications': department.get_notifications(),
            'projects': Project.objects.filter(is_active=True),
            'departments': Department.objects.all(),
            'tasks': {
                'progress': Task.objects.filter(state='progress', from_department=department).count(),
                'queue': Task.objects.filter(state='queue', from_department=department).count(),
                'need_to_check': Task.objects.filter(state='need-to-check', from_department=department).count(),
                'hold': Task.objects.filter(state='hold', from_department=department).count(),
                'need_to_replan': Task.objects.filter(state='need-to-replan', from_department=department).count(),
                'finished': Task.objects.filter(state='finished', from_department=department).count(),
            }
        }
        return render(request, self.template_name, context)
