from django.shortcuts import render
from django.views.generic import View
from public.models import Department, Project
from account.auth.decorators import user_role_required_cbv


class Index(View):
    template_name = 'production/index.html'

    @user_role_required_cbv(['production_user'])
    def get(self, request):
        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
            'departments': Department.objects.all(),
            'projects': Project.objects.filter(is_active=True),
        }
        return render(request, self.template_name, context)
