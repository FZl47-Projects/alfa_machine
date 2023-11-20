from django.shortcuts import render
from django.views.generic import View
from public.models import Department, Project
from account.auth.decorators import user_role_required_cbv


class Index(View):
    template_name = 'production/index.html'

    @user_role_required_cbv(['production_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)

        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
            'departments': Department.objects.all(),
            'projects': projects,
            'ongoing_projects': projects.filter(status__in=['checking', 'paused', 'under_construction'])[:4],
        }
        return render(request, self.template_name, context)
