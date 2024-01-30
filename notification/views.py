from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import View
from public.models import Project, Department
from . import forms, models


class NotificationAdd(LoginRequiredMixin, View):
    template_name = 'notification/notify/add.html'

    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True),
            'departments': Department.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST.copy()
        # set additional values
        user = request.user
        data['from_department'] = user.department
        f = forms.NotificationDepartmentCreate(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect('notification:notification__add')
        notif = f.save(commit=False)
        projects = data.getlist('projects')
        if 'other' in projects:
            notif.projects_type = 'other'
            notif.save()
        else:
            notif.projects_type = 'selected'
            notif.save()
            notif.projects.add(*projects)
        notif.to_departments.add(*data.getlist('to_departments'))
        messages.success(request, 'اعلان با موفقیت ایجاد شد')
        return redirect('notification:notification__add')


class NotificationList(LoginRequiredMixin, View):
    USER_ACCESS_TO_ALL = ('super_user',)
    pagination_count = 25
    template_name = 'notification/notify/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def get_notifications(self):
        """
            get notifications by user department
        """
        notifications = models.NotificationDepartment.objects.all()
        user = self.request.user
        if user.role in self.USER_ACCESS_TO_ALL:
            return notifications
        notifications = notifications.filter(to_departments__in=[user.department])
        return notifications

    def sort(self, notifications):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            notifications = notifications.order_by('-id')
        elif sort_by == 'oldest':
            notifications = notifications.order_by('id')
        elif sort_by == 'high-priority':
            notifications = notifications.order_by('-priority')
        return notifications

    def filter(self, notifications):
        qs = self.request.GET
        search = qs.get('search', None)
        projects = qs.get('projects', 'all')
        to_departments = qs.get('to_departments', 'all')

        if search:
            notifications = notifications.filter(title__icontains=search)

        if projects == 'other':
            notifications = notifications.filter(projects_type='other')
        else:
            if (projects != 'all') and (projects.isdigit()):
                notifications = notifications.filter(projects__in=[projects])

        if (to_departments != 'all') and (to_departments.isdigit()):
            notifications = notifications.filter(to_departments__in=[to_departments])

        return notifications

    def get(self, request):
        notifications = self.get_notifications()
        notifications = self.filter(notifications)
        notifications = self.sort(notifications)
        pagination, notifications = self.pagination(notifications)
        context = {
            'pagination': pagination,
            'notifications': notifications,
            'projects': Project.objects.filter(is_active=True),
            'departments': Department.objects.all(),
        }
        return render(request, self.template_name, context)


class NotificationDetail(LoginRequiredMixin, View):
    template_name = 'notification/notify/detail.html'

    def get(self, request, notification_id):
        notification = get_object_or_404(models.NotificationDepartment, id=notification_id)
        department = request.user.department
        if department in notification.get_to_departments() and department != notification.from_department:
            # seen notification
            _, _ = models.NotificationDepartmentSeen.objects.get_or_create(
                notification=notification,
                department=department
            )
        context = {
            'notification': notification,
            # permissions
            'has_perm_to_modify': notification.has_perm_to_modify(request.user)
        }
        return render(request, self.template_name, context)


class NotificationDelete(LoginRequiredMixin, View):

    def get(self, request, notification_id):
        notification = get_object_or_404(models.NotificationDepartment, id=notification_id)
        if not notification.has_perm_to_modify(request.user):
            raise PermissionDenied
        notification.delete()
        messages.success(request, 'اعلان با موفقیت حذف شد')
        return redirect('notification:notification__list')


class NotificationUpdate(LoginRequiredMixin, View):

    def post(self, request, notification_id):
        notification = get_object_or_404(models.NotificationDepartment, id=notification_id)
        if not notification.has_perm_to_modify(request.user):
            raise PermissionDenied
        f = forms.NotificationDepartmentUpdate(request.POST, files=request.FILES, instance=notification)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(notification.get_absolute_url())
        f.save()
        messages.success(request, 'اعلان با موفقیت بروزرسانی شد')
        return redirect(notification.get_absolute_url())


class NotificationSeenAll(LoginRequiredMixin, View):

    def get(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        department = request.user.department
        notifications = department.get_unread_notifications()
        notifications_object = []
        for n in notifications:
            notifications_object.append(
                models.NotificationDepartmentSeen(department=department, notification=n)
            )
        models.NotificationDepartmentSeen.objects.bulk_create(notifications_object)
        return redirect(referer_url or '/')
