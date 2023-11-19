from django.shortcuts import render
from django.views.generic import View
from public.models import Project, Department
from account.auth.decorators import user_role_required_cbv


class Index(View):
    template_name = 'technical/index.html'

    @user_role_required_cbv(['technical_user'])
    def get(self, request):
        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
            'departments': Department.objects.all(),
            'projects': Project.objects.filter(is_active=True, status__in=['checking', 'paused', 'under_construction'])[:4],
        }
        return render(request, self.template_name, context)
