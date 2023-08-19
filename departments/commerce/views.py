from django.shortcuts import render
from django.views.generic import View
from public.models import Project, Department
from account.auth.decorators import user_role_required_cbv


class Index(View):
    template_name = 'commerce/index.html'

    @user_role_required_cbv(['commerce_user'])
    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True),
            'departments': Department.objects.all(),
        }
        return render(request, self.template_name, context)

