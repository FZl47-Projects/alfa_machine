from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from public.models import Project, Task, Department, Inquiry
from account.auth.decorators import user_role_required_cbv
from account.models import User
from public.models import Department


class Index(View):
    template_name = 'general/index.html'

    @user_role_required_cbv(['super_user'])
    def get(self, request):
        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
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

class UsersList(View):
    template_name = 'general/users_list.html'
    @user_role_required_cbv(['super_user'])
    def get(self, request):
        context = {
            'users': User.objects.all()
        }
        return render(request, self.template_name, context)

class DepartmentsList(View):
    template_name = 'general/departments_list.html'
    @user_role_required_cbv(['super_user'])
    def get(self, request):
        context= {
            'departments': Department.objects.all()
        }
        return render(request, self.template_name, context)
def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    department.delete()
    return redirect ('departments.general:departments_list')
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect ('departments.general:users_list')
        