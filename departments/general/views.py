from django.shortcuts import render
from django.views.generic import View
from public.models import Project, Task, Department, Inquiry
from account.auth.decorators import user_role_required_cbv


class Index(View):
    template_name = 'general/index.html'

    @user_role_required_cbv(['super_user'])
    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True)[:4],
            'inquiries': Inquiry.objects.filter(status=None)[:4],
            'departments': Department.objects.all(),
            'tasks': {
                'progress': Task.objects.filter(state='progress').count(),
                'queue': Task.objects.filter(state='queue').count(),
                'finished': Task.objects.filter(state='finished').count(),
                'need_to_check': Task.objects.filter(state='need-to-check').count(),
            }
        }
        return render(request, self.template_name, context)
