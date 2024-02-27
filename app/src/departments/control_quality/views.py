from django.shortcuts import render
from django.views.generic import View
from public.models import Project
from account.auth.decorators import user_role_required_cbv


class Index(View):
    template_name = 'control_quality/index.html'

    @user_role_required_cbv(['control_quality_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)
        context = {
            'projects': projects,
        }
        return render(request, self.template_name, context)
