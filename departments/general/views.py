from django.shortcuts import render
from django.views.generic import View
from public.models import Project, Task, Department


class Index(View):
    template_name = 'general/index.html'

    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True),
            'departments': Department.objects.all(),
            'tasks': {
                'progress': Task.objects.filter(state='progress').count(),
                'queue': Task.objects.filter(state='queue').count(),
                'finished': Task.objects.filter(state='finished').count(),
                'need_to_check': Task.objects.filter(state='need-to-check').count(),
            }
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass
