from django.shortcuts import render
from django.views.generic import View
from .models import NotificationDepartment


class NotificationDepartmentList(View):
    template_name = 'notification/list.html'

    def get(self, request):
        user_department = request.user.department
        notifications = NotificationDepartment.objects.filter(from_department=user_department,to_department=user_department)
        context = {
            'notifications': notifications
        }
        return render(request, self.template_name, context)
