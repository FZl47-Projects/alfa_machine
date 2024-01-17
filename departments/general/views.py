from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from public.models import Project, Task, Department, Inquiry
from account.auth.decorators import user_role_required_cbv
from account.models import User
from public.models import Department


class Index(View):
    template_name = 'general/index.html'

    @user_role_required_cbv(['super_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)

        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
            'projects': projects,
            'ongoing_projects': projects.filter(status__in=['checking', 'paused', 'under_construction'])[:4],
            'inquiries': Inquiry.objects.all(),
            'departments': Department.objects.all(),
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
        context = {
            'departments': Department.objects.all()
        }
        return render(request, self.template_name, context)


def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    department.delete()
    return redirect('departments.general:departments_list')


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, 'کاربر با موفقیت حذف شد')
    return redirect('departments.general:users_list')
