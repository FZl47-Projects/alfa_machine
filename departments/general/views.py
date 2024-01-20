import json

from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Count
from django.contrib import messages
from account.auth.decorators import user_role_required_cbv
from account.models import User
from public.models import Project, TaskMaster, Department, Inquiry


class Index(View):
    template_name = 'general/index.html'

    @user_role_required_cbv(['super_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True).annotate(task_count=Count('task'))

        # chart data
        chart = {
            'project__tasks_count': json.dumps(list(projects.values_list('task_count', flat=True))),
            'project__names': json.dumps(list(projects.values_list('name', flat=True))),
        }

        context = {
            'projects': projects,
            'inquiries': Inquiry.objects.all(),
            'departments': Department.objects.all(),
            'users': User.objects.all(),
            'task_masters': TaskMaster.objects.all(),
            'chart': chart
        }
        return render(request, self.template_name, context)


# class UsersList(View):
#     template_name = 'general/users_list.html'
#
#     @user_role_required_cbv(['super_user'])
#     def get(self, request):
#         context = {
#             'users': User.objects.all()
#         }
#         return render(request, self.template_name, context)


# class DepartmentsList(View):
#     template_name = 'general/departments_list.html'
#
#     @user_role_required_cbv(['super_user'])
#     def get(self, request):
#         context = {
#             'departments': Department.objects.all()
#         }
#         return render(request, self.template_name, context)

#
# def delete_department(request, department_id):
#     department = Department.objects.get(id=department_id)
#     department.delete()
#     return redirect('departments.general:departments_list')

#
# def delete_user(request, user_id):
#     user = User.objects.get(id=user_id)
#     user.delete()
#     messages.success(request, 'کاربر با موفقیت حذف شد')
#     return redirect('departments.general:users_list')
