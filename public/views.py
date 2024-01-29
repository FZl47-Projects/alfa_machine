from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib import messages
from django.db.models import Q, Count

from account.auth.decorators import user_role_required_cbv
from notification.models import NotificationDepartment
from notification.utils import create_notification
from core.utils import form_validate_err
from public import models, forms


class Success(View):
    def get(self, request):
        return HttpResponse('عملیات با موفقیت انجام شد')


class Error(View):
    def get(self, request):
        return HttpResponse('عملیات با خطا مواجه شد')


class Index(View):
    def get(self, request):
        return redirect(request.user.get_absolute_url_dashboard())


class ProjectDetail(LoginRequiredMixin, View):
    template_name = 'public/project/detail.html'

    def get(self, request, project_id):
        project = get_object_or_404(models.Project, id=project_id)
        context = {
            'has_perm_to_modify': project.has_perm_to_modify(request.user),
            'project': project,
            'task_masters': models.TaskMaster.objects.all()
        }
        return render(request, self.template_name, context)


class ProjectList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/project/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def filter(self, projects):
        qs = self.request.GET
        search = qs.get('search', None)
        task_master = qs.get('task_master', 'all')
        project_status = qs.get('project_status', 'all')

        if search:
            projects = projects.filter(name__icontains=search)

        if (task_master != 'all') and (task_master.isdigit()):
            projects = projects.filter(task_master_id=task_master)

        if project_status != 'all':
            projects = projects.filter(status=project_status)

        # filter by start and end date project
        time_start_gt = qs.get('time_start__gt', None)
        time_start_lt = qs.get('time_start__lt', None)
        time_end_gt = qs.get('time_end__gt', None)
        time_end_lt = qs.get('time_end__lt', None)

        if time_start_gt:
            projects = projects.filter(time_start__gt=time_start_gt)

        if time_start_lt:
            projects = projects.filter(time_start__lt=time_start_lt)

        if time_end_gt:
            projects = projects.filter(time_end__gt=time_end_gt)

        if time_end_lt:
            projects = projects.filter(time_end__lt=time_end_lt)

        return projects

    def get(self, request):
        projects = models.Project.objects.filter(is_active=True)
        projects = self.filter(projects)
        pagination, projects = self.pagination(projects)
        context = {
            'projects': projects,
            'pagination': pagination,
            'task_masters': models.TaskMaster.objects.all()
        }
        return render(request, self.template_name, context)


class ProjectAdd(LoginRequiredMixin, View):
    template_name = 'public/project/add.html'

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def get(self, request):
        context = {
            'task_masters': models.TaskMaster.objects.all()
        }
        inquiry_id = request.GET.get('inquiry-id', None)
        if inquiry_id:
            context['inquiry'] = models.Inquiry.objects.get(id=inquiry_id, project=None)

        return render(request, self.template_name, context)

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def post(self, request):
        data = request.POST
        f = forms.ProjectCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('public:project__add')
        project = f.save()
        messages.success(request, 'پروژه با موفقیت ایجاد شد')
        return redirect(project.get_absolute_url())


class ProjectUpdate(LoginRequiredMixin, View):

    def post(self, request, project_id):
        project = get_object_or_404(models.Project, id=project_id)
        if not project.has_perm_to_modify(request.user):
            raise PermissionDenied
        f = forms.ProjectUpdate(data=request.POST, instance=project)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(project.get_absolute_url())
        f.save()
        messages.success(request, 'پروژه با موفقیت بروزرسانی شد')
        return redirect(project.get_absolute_url())


class ProjectDelete(LoginRequiredMixin, View):

    def get(self, request, project_id):
        if not models.Project.has_perm_to_modify(request.user):
            raise PermissionDenied
        project = models.Project.objects.get(id=project_id)
        project.delete()
        messages.success(request, 'پروژه با موفقیت حذف شد')
        return redirect('public:project__list')


# class ProjectFile(LoginRequiredMixin, View):
#
#     def search(self, request, items):
#         search = request.GET.get('search', None)
#         if not search:
#             return items
#         items = items.filter(name__icontains=search)
#         return items
#
#     @user_role_required_cbv(
#         ['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user', 'control_quality_user',
#          'technical_user', 'production_user'])
#     def get(self, request):
#         projects = models.Project.objects.filter(is_active=True)
#         projects = self.search(request, projects)
#         context = {
#             'projects': projects
#         }
#         return render(request, 'public/project/file/list.html', context)
#
#     def post(self, request):
#         referer_url = request.META.get('HTTP_REFERER', None)
#         data = request.POST.copy()
#         # set additional values
#         data['from_department'] = request.user.department
#
#         f = forms.ProjectFile(data, request.FILES)
#         if form_validate_err(request, f) is False:
#             return redirect(referer_url or '/error')
#         obj = f.save()
#
#         # Create notification for each department
#         notif_title = 'اعلان آپلود فایل پروژه'
#         notif_description = f'فایل جدید برای پروژه ({obj.project.name})'
#         create_notification(from_department=obj.from_department, title=notif_title, description=notif_description,
#                             projects=obj.project, all_departments=True)
#
#         messages.success(request, 'عملیات مورد نظر با موفقیت انجام شد')
#         return redirect(referer_url or '/success')


# class ProjectDetailFileList(LoginRequiredMixin, View):
#
#     def search(self, request, items):
#         search = request.GET.get('search', None)
#         if not search:
#             return items
#         items = items.filter(name__icontains=search)
#         return items
#
#     def sort(self, request, items):
#         sort_by = request.GET.get('sort_by', 'latest')
#         if sort_by == 'latest':
#             items = items.order_by('-id')
#         elif sort_by == 'oldest':
#             items = items.order_by('id')
#         return items
#
#     def filter(self, request, items):
#         # search
#         items = self.search(request, items)
#         # filter
#         filter_by = request.GET.get('filter_by')
#         if filter_by and filter_by.isdigit():
#             items = items.filter(from_department__id=filter_by)
#         # sort
#         items = self.sort(request, items)
#         return items
#
#     @user_role_required_cbv(
#         ['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user', 'control_quality_user',
#          'technical_user', 'production_user'])
#     def get(self, request, project_id):
#         project = models.Project.objects.get(id=project_id, is_active=True)
#         files = project.get_files()
#         # search & filter
#         files = self.filter(request, files)
#         context = {
#             'files': files,
#             'project': project,
#             'departments': models.Department.objects.all()
#         }
#         return render(request, 'public/project/file/detail.html', context)


# class TaskOwner(LoginRequiredMixin, View):
#     """
#         get tasks who created and crud task with post method
#     """
#
#     def pagination(self, request, objects, count=20):
#         paginator = Paginator(objects, count)  # show how many objects per page.
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         return page_obj, page_obj.object_list
#
#     def search(self, request, tasks):
#         search = request.GET.get('search', None)
#         if not search:
#             return tasks
#         lookup = Q(name__icontains=search) | Q(from_department__name__icontains=search)
#         tasks = tasks.filter(lookup)
#         return tasks
#
#     def sort(self, request, tasks):
#         sort_by = request.GET.get('sort_by', 'latest')
#         if sort_by == 'latest':
#             tasks = tasks.order_by('-id')
#         elif sort_by == 'oldest':
#             tasks = tasks.order_by('id')
#         return tasks
#
#     def get(self, request):
#         # get task list by type state
#         task_state = request.GET.get('task_state', None)
#         department = request.user.department
#
#         if request.user.role in ('super_user',):
#             tasks = models.Task.objects.filter(is_active=True)
#         else:
#             tasks = models.Task.objects.filter(is_active=True, from_department=department)
#
#         if task_state:
#             tasks = tasks.filter(state=task_state)
#
#         tasks = self.search(request, tasks)
#         tasks = self.sort(request, tasks)
#         paginator, tasks = self.pagination(request, tasks)
#         context = {
#             'tasks': tasks,
#             'paginator': paginator,
#             'departments': models.Department.objects.all(),
#             'projects': models.Project.objects.filter(is_active=True)
#         }
#
#         return render(request, 'public/task/list-state.html', context)
#
#     def post(self, request, task_id):
#         type_request = request.POST.get('type_request', None)
#         referer_url = request.META.get('HTTP_REFERER', None)
#
#         if type_request == 'update':
#             data = request.POST
#             task_obj = models.Task.objects.get(id=task_id, from_department=request.user.department)
#
#             f = forms.TaskUpdateForm(data, request.FILES, instance=task_obj)
#             if form_validate_err(request, f) is False:
#                 return redirect(referer_url or '/error')
#             task = f.save()
#
#             notif = NotificationDepartment.objects.create(
#                 from_department=request.user.department,
#                 department=task.to_department,
#                 title='اعلان بروزرسانی تسک',
#                 description=f'بروزرسانی برای تسک: "{task.name}"'
#             )
#             notif.projects.set([task.project])
#
#             messages.success(request, 'تسک با موفقیت بروزرسانی شد')
#         elif type_request == 'delete':
#             models.Task.objects.get(id=task_id).delete()
#
#         return redirect(referer_url or '/success')
#
#
# class TaskOwnerDepartment(View):
#     template_name = 'public/task/department-each.html'
#
#     def pagination(self, request, objects, count=20):
#         paginator = Paginator(objects, count)  # show how many objects per page.
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         return page_obj, page_obj.object_list
#
#     def search(self, request, tasks):
#         search = request.GET.get('search', None)
#         if not search:
#             return tasks
#         lookup = Q(name__icontains=search) | Q(from_department__name__icontains=search)
#         tasks = tasks.filter(lookup)
#         return tasks
#
#     def sort(self, request, tasks):
#         sort_by = request.GET.get('sort_by', 'latest')
#         if sort_by == 'latest':
#             tasks = tasks.order_by('-id')
#         elif sort_by == 'oldest':
#             tasks = tasks.order_by('id')
#         return tasks
#
#     def get(self, request, department_id):
#         department = models.Department.objects.get(id=department_id)
#         tasks = models.Task.objects.filter(to_department=department)
#
#         tasks = self.search(request, tasks)
#         tasks = self.sort(request, tasks)
#         paginator, tasks = self.pagination(request, tasks)
#
#         context = {
#             'tasks': tasks,
#             'paginator': paginator,
#             'department': department,
#             'departments': models.Department.objects.all(),
#             'projects': models.Project.objects.filter(is_active=True)
#         }
#
#         return render(request, self.template_name, context)


class TaskAdd(LoginRequiredMixin, View):
    template_name = 'public/task/add.html'

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request):
        context = {
            'projects': models.Project.objects.filter(is_active=True),
            'departments': models.Department.objects.all()
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def post(self, request):
        data = request.POST.copy()
        # set default values
        data['allocator_user'] = request.user
        data['from_department'] = request.user.department

        f = forms.TaskCreate(data, request.FILES)
        if not form_validate_err(request, f):
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect('public:task__add')
        task = f.save()
        # TODO: should use in signals
        # create status task(queue)
        models.TaskStatus.objects.create(
            department=task.to_department,
            task=task,
            status='queue',
            description='ایجاد به صورت خودکار'
        )
        # Create notification for department
        # TODO: should be refactor and completed
        notif_title = 'اطلاعیه تسک جدید'
        notif_description = f'عنوان تسک: "{task.name}"'
        create_notification(
            from_department=request.user.department,
            title=notif_title, description=notif_description,
            projects=task.project, departments=[task.to_department]
        )
        messages.success(request, 'تسک با موفقیت ایجاد شد')
        return redirect('public:task__add')


class TaskList(LoginRequiredMixin, View):
    USER_ACCESS_TO_ALL = ('super_user', 'control_project_user')
    pagination_count = 25
    template_name = 'public/task/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def get_tasks(self):
        """
            get tasks by user department
        """
        tasks = models.Task.objects.all()
        user = self.request.user
        if user.role in self.USER_ACCESS_TO_ALL:
            return tasks
        tasks = tasks.filter(to_department=user.department)
        return tasks

    def sort(self, tasks):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            tasks = tasks.order_by('-id')
        elif sort_by == 'oldest':
            tasks = tasks.order_by('id')
        elif sort_by == 'priority_high':
            tasks = tasks.order_by('-priority')
        return tasks

    def filter(self, tasks):
        qs = self.request.GET
        search = qs.get('search', None)
        project = qs.get('project', 'all')
        status = qs.get('status', 'all')
        to_department = qs.get('to_department', 'all')

        if search:
            tasks = tasks.filter(name__icontains=search)

        if (project != 'all') and (project.isdigit()):
            tasks = tasks.filter(project_id=project)

        if (to_department != 'all') and (to_department.isdigit()):
            tasks = tasks.filter(to_department_id=to_department)

        if status != 'all':
            if status == 'queue':
                lookup = Q(taskstatus__status=status) | Q(taskstatus=None)
                tasks = tasks.filter(lookup).distinct()
            else:
                tasks = tasks.filter(taskstatus__status=status)

        # filter by start and end date tasks
        time_start_gt = qs.get('time_start__gt', None)
        time_start_lt = qs.get('time_start__lt', None)
        time_end_gt = qs.get('time_end__gt', None)
        time_end_lt = qs.get('time_end__lt', None)

        if time_start_gt:
            tasks = tasks.filter(time_start__gt=time_start_gt)

        if time_start_lt:
            tasks = tasks.filter(time_start__lt=time_start_lt)

        if time_end_gt:
            tasks = tasks.filter(time_end__gt=time_end_gt)

        if time_end_lt:
            tasks = tasks.filter(time_end__lt=time_end_lt)

        return tasks

    def get(self, request):
        tasks = self.get_tasks()
        tasks = self.filter(tasks)
        tasks = self.sort(tasks)
        pagination, tasks = self.pagination(tasks)
        context = {
            'pagination': pagination,
            'tasks': tasks,
            'task_status': models.TaskStatus.STATUS_OPTIONS,
            'projects': models.Project.objects.filter(is_active=True),
            'departments': models.Department.objects.all(),
            # permissions
            'has_perm_to_send_notify': models.Task.has_perm_to_send_notify(request.user)
        }
        return render(request, self.template_name, context)


class TaskDetail(LoginRequiredMixin, View):
    USER_FULL_ACCESS = ('super_user', 'control_project_user')
    template_name = 'public/task/detail.html'

    def get(self, request, task_id):
        user = request.user
        task = get_object_or_404(models.Task, id=task_id)
        if task.to_department != user.department and not (user.role in self.USER_FULL_ACCESS):
            raise PermissionDenied
        context = {
            'task': task,
            'task_status': models.TaskStatus.STATUS_OPTIONS,
            # permissions
            'has_perm_to_modify': task.has_perm_to_modify(request.user),
            'has_perm_to_send_notify': task.has_perm_to_send_notify(request.user)
        }
        return render(request, self.template_name, context)


class TaskDelete(LoginRequiredMixin, View):

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request, task_id):
        task = get_object_or_404(models.Task, id=task_id)
        task.delete()
        messages.success(request, 'تسک با موفقیت حذف شد')
        return redirect('public:task__list')


class TaskUpdate(LoginRequiredMixin, View):

    def post(self, request, task_id):
        if not models.Task.has_perm_to_modify(request.user):
            raise PermissionDenied
        task = get_object_or_404(models.Task, id=task_id)
        f = forms.TaskUpdate(data=request.POST, files=request.FILES, instance=task)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect(task.get_absolute_url())
        task = f.save()
        messages.success(request, 'تسک با موفقیت بروزرسانی شد')
        return redirect(task.get_absolute_url())


class TaskStatusAdd(LoginRequiredMixin, View):

    def post(self, request, task_id):
        user = request.user
        task = get_object_or_404(models.Task, id=task_id, to_department=user.department)
        data = request.POST.copy()
        # set additional values
        data['allocator_user'] = user
        data['department'] = user.department
        data['task'] = task
        f = forms.TaskStatusCreate(data=data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect(task.get_absolute_url())
        task_status = f.save()
        messages.success(request, 'وضعیت تسک با موفقیت ایجاد شد')
        return redirect(task.get_absolute_url())


class TaskRemind(LoginRequiredMixin, View):
    # TODO: should be refactor and completed

    def post(self, request, task_id):
        referer_url = request.META.get('HTTP_REFERER', None)

        user = request.user
        department = user.department
        task = get_object_or_404(models.Task, id=task_id)

        # Create notification for department
        notif_title = 'یادآوری انجام تسک'
        notif_description = f'یادآوری جهت انجام تسک ({task.name})'
        create_notification(
            from_department=department,
            title=notif_title, description=notif_description,
            projects=task.project, departments=[task.to_department]
        )

        messages.success(request, 'عملیات مورد نظر با موفقیت ایجاد شد')

        return redirect(referer_url or '/success')


class InquiryAdd(LoginRequiredMixin, View):
    template_name = 'public/inquiry/add.html'

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user'])
    def get(self, request):
        context = {
            'inquiry_states': models.Inquiry.STATE_OPTIONS,
            'task_masters': models.TaskMaster.objects.all()
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user'])
    def post(self, request):
        data = request.POST.copy()
        # set additional values
        data['from_department'] = request.user.department

        f = forms.InquiryAdd(data)
        if form_validate_err(request, f) is False:
            return redirect('public:inquiry__add')
        inquiry = f.save()
        messages.success(request, 'استعلام با موفقیت ایجاد شد')
        return redirect(inquiry.get_absolute_url())


class InquiryList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/inquiry/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def filter(self, inquiries):
        qs = self.request.GET
        search = qs.get('search', None)
        task_master = qs.get('task_master', 'all')
        state = qs.get('state', 'all')

        if search:
            lookup = Q(title__icontains=search)
            if search.isdigit():
                lookup = lookup | Q(number_id=search)
            inquiries = inquiries.filter(lookup)

        if (task_master != 'all') and (task_master.isdigit()):
            inquiries = inquiries.filter(task_master_id=task_master)

        if state != 'all':
            inquiries = inquiries.filter(state=state)

        # filter by time
        time_deadline_response_gt = qs.get('time_deadline_response__gt', None)
        time_deadline_response_lt = qs.get('time_deadline_response__lt', None)
        time_submit_gt = qs.get('time_submit__gt', None)
        time_submit_lt = qs.get('time_submit__lt', None)

        if time_deadline_response_gt:
            inquiries = inquiries.filter(time_deadline_response_gt=time_deadline_response_gt)

        if time_deadline_response_lt:
            inquiries = inquiries.filter(time_deadline_response_lt=time_deadline_response_lt)

        if time_submit_gt:
            inquiries = inquiries.filter(time_submit_gt=time_submit_gt)

        if time_submit_lt:
            inquiries = inquiries.filter(time_submit_lt=time_submit_lt)

        return inquiries

    def sort(self, inquiries):
        sort_by = self.request.GET.get('sort_by', 'latest')

        if sort_by == 'latest':
            inquiries = inquiries.order_by('-id')
        elif sort_by == 'oldest':
            inquiries = inquiries.order_by('id')
        return inquiries

    def get(self, request):
        inquiries = models.Inquiry.objects.all()
        inquiries = self.filter(inquiries)
        inquiries = self.sort(inquiries)
        pagination, inquiries = self.pagination(inquiries)

        context = {
            'pagination': pagination,
            'inquiries': inquiries,
            'departments': models.Department.objects.all(),
            'task_masters': models.TaskMaster.objects.all(),
            'inquiry_states': models.Inquiry.STATE_OPTIONS,
        }

        return render(request, self.template_name, context)


class InquiryDetail(LoginRequiredMixin, View):
    template_name = 'public/inquiry/detail.html'

    def get_inquiry_files(self, inquiry):
        department = self.request.user.department
        # get file for this department
        lookup = Q(from_department=department) | Q(to_departments__in=[department])
        files = inquiry.get_files().filter(lookup).distinct()
        return files

    def get(self, request, inquiry_id):
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        context = {
            'inquiry': inquiry,
            'inquiry_files': self.get_inquiry_files(inquiry),
            'task_masters': models.TaskMaster.objects.all(),
            'departments': models.Department.objects.all(),
            # permissions
            'has_perm_to_modify': inquiry.has_perm_to_modify(request.user),
            'has_perm_to_manage_status': inquiry.has_perm_to_manage_status(request.user),
        }
        return render(request, self.template_name, context)


class InquiryDelete(LoginRequiredMixin, View):

    def get(self, request, inquiry_id):
        if not models.Inquiry.has_perm_to_modify(request.user):
            raise PermissionDenied
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        inquiry.delete()
        messages.success(request, 'استعلام با موفقیت حذف شد')
        return redirect('public:inquiry__list')


class InquiryUpdate(LoginRequiredMixin, View):

    def post(self, request, inquiry_id):
        if not models.Inquiry.has_perm_to_modify(request.user):
            raise PermissionDenied
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        data = request.POST
        f = forms.InquiryUpdate(data, instance=inquiry)
        if form_validate_err(request, f) is False:
            return redirect(inquiry.get_absolute_url())
        f.save()
        messages.success(request, 'استعلام با موفقیت بروزرسانی شد')
        return redirect(inquiry.get_absolute_url())


class InquiryStatusModify(LoginRequiredMixin, View):

    def post(self, request, inquiry_id):
        if not models.Inquiry.has_perm_to_manage_status(request.user):
            raise PermissionDenied
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        data = request.POST.copy()
        # set additional values
        data['inquiry'] = inquiry
        inquiry_status = getattr(inquiry, 'status', None)
        f = forms.InquiryStatusModify(data, files=request.FILES, instance=inquiry_status)
        if not form_validate_err(request, f):
            return redirect(inquiry.get_absolute_url())
        f.save()
        messages.success(request, 'وضعیت استعلام با موفقیت ثبت و بروزرسانی شد')
        return redirect(inquiry.get_absolute_url())


class InquiryFileAdd(LoginRequiredMixin, View):

    def post(self, request, inquiry_id):
        inquiry = get_object_or_404(models.Inquiry, id=inquiry_id)
        data = request.POST.copy()
        user = request.user
        # set additional values
        data['inquiry'] = inquiry
        data['from_department'] = user.department
        data['allocator_user'] = user
        f = forms.InquiryFile(data, request.FILES)
        if not form_validate_err(request, f):
            return redirect(inquiry.get_absolute_url())
        # create and upload files
        files_object = []
        files = request.FILES.getlist('files')
        for file in files:
            files_object.append(models.File(file=file))
        files_object = models.File.objects.bulk_create(files_object)
        inquiry_file = f.save()
        inquiry_file.files.add(*files_object)
        messages.success(request, 'فایل پیوست با ایجاد و اپلود شد')
        return redirect(inquiry.get_absolute_url())


class InquiryFileDelete(LoginRequiredMixin, View):

    def get(self, request, inquiry_id, inquiry_file_id):
        inquiry_file = get_object_or_404(models.InquiryFile, id=inquiry_file_id, inquiry_id=inquiry_id)
        if inquiry_file.from_department != request.user.department:
            raise PermissionDenied
        inquiry_file.delete()
        messages.success(request, 'فایل استعلام با موفقیت حذف شد')
        return redirect(inquiry_file.inquiry.get_absolute_url())


class TaskMasterAdd(LoginRequiredMixin, View):
    template_name = 'public/task_master/add.html'

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def get(self, request):
        return render(request, self.template_name)

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def post(self, request):
        data = request.POST
        f = forms.TaskMasterCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect('public:task_master__add')
        task_master = f.save()
        messages.success(request, 'مشتری با موفقیت ایجاد شد')
        return redirect(task_master.get_absolute_url())


class TaskMasterList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/task_master/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def filter(self, task_masters):
        qs = self.request.GET
        search = qs.get('search', None)
        if search:
            task_masters = task_masters.filter(name__icontains=search)
        return task_masters

    def sort(self, task_masters):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            task_masters = task_masters.order_by('-id')
        elif sort_by == 'oldest':
            task_masters = task_masters.order_by('id')
        elif sort_by == 'most-project':
            task_masters = task_masters.annotate(c=Count('projects')).order_by('-c')

        return task_masters

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def get(self, request):
        task_masters = models.TaskMaster.objects.all()
        task_masters = self.filter(task_masters)
        task_masters = self.sort(task_masters)
        pagination, task_masters = self.pagination(task_masters)
        context = {
            'pagination': pagination,
            'task_masters': task_masters
        }
        return render(request, self.template_name, context)


class TaskMasterDetail(LoginRequiredMixin, View):
    template_name = 'public/task_master/detail.html'

    @user_role_required_cbv(['super_user', 'commerce_user', 'procurement_commerce_user', 'control_project_user'])
    def get(self, request, task_master_id):
        task_master = get_object_or_404(models.TaskMaster, id=task_master_id)
        context = {
            'task_master': task_master,
            # permissions
            'has_perm_to_modify': task_master.has_perm_to_modify(request.user),
            'has_perm_to_delete': task_master.has_perm_to_delete(request.user),
        }
        return render(request, self.template_name, context)


class TaskMasterDelete(LoginRequiredMixin, View):
    def get(self, request, task_master_id):
        if not models.TaskMaster.has_perm_to_delete(request.user):
            raise PermissionDenied
        task_master = get_object_or_404(models.TaskMaster, id=task_master_id)
        task_master.delete()
        messages.success(request, 'مشتری با موفقیت حذف شد')
        return redirect('public:task_master__list')


class TaskMasterUpdate(LoginRequiredMixin, View):
    def post(self, request, task_master_id):
        if not models.TaskMaster.has_perm_to_modify(request.user):
            raise PermissionDenied
        task_master = get_object_or_404(models.TaskMaster, id=task_master_id)
        f = forms.TaskMasterUpdate(request.POST, instance=task_master)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(task_master.get_absolute_url())
        f.save()
        messages.success(request, 'مشتری با موفقیت بروزرسانی شد')
        return redirect(task_master.get_absolute_url())


class DepartmentAdd(LoginRequiredMixin, View):
    template_name = 'public/department/add.html'

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request):
        return render(request, self.template_name)

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def post(self, request):
        data = request.POST
        f = forms.DepartmentCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('public:department__add')
        f.save()
        messages.success(request, 'واحد با موفقیت ایجاد شد')
        return redirect('public:department__add')


class DepartmentList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/department/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def sort(self, departments):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            departments = departments.order_by('-id')
        elif sort_by == 'oldest':
            departments = departments.order_by('id')
        elif sort_by == 'most-tasks':
            departments = departments.annotate(c=Count('task')).order_by('-c')
        return departments

    def filter(self, departments):
        qs = self.request.GET
        search = qs.get('search', None)
        if search:
            departments = departments.filter(name__icontains=search)
        return departments

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request):
        departments = models.Department.objects.all()
        departments = self.filter(departments)
        departments = self.sort(departments)
        pagination, departments = self.pagination(departments)
        context = {
            'pagination': pagination,
            'departments': departments,
        }
        return render(request, self.template_name, context)


class DepartmentDetail(LoginRequiredMixin, View):
    template_name = 'public/department/detail.html'

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request, department_id):
        department = get_object_or_404(models.Department, id=department_id)
        context = {
            'department': department,
            # permissions
            'has_perm_to_modify': department.has_perm_to_modify(request.user),
            'has_perm_to_delete': department.has_perm_to_delete(request.user),
        }
        return render(request, self.template_name, context)


class DepartmentDelete(LoginRequiredMixin, View):
    template_name = 'public/department/detail.html'

    def get(self, request, department_id):
        if not models.Department.has_perm_to_delete(request.user):
            raise PermissionDenied
        department = get_object_or_404(models.Department, id=department_id)
        department.delete()
        messages.success(request, 'واحد با موفقیت حذف شد')
        return redirect('public:department__list')


class DepartmentUpdate(LoginRequiredMixin, View):
    def post(self, request, department_id):
        if not models.Department.has_perm_to_modify(request.user):
            raise PermissionDenied
        department = get_object_or_404(models.Department, id=department_id)
        f = forms.DepartmentUpdate(request.POST, instance=department)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(department.get_absolute_url())
        f.save()
        messages.success(request, 'واحد با موفقیت بروزرسانی شد')
        return redirect(department.get_absolute_url())


class ProjectFileAdd(LoginRequiredMixin, View):
    template_name = 'public/project_file/add.html'

    def get(self, request):
        context = {
            'projects': models.Project.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST.copy()
        # set additional values
        user = request.user
        data['allocator_user'] = user
        data['from_department'] = user.department
        f = forms.ProjectFileCreate(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('public:project_file__add')
        f.save()
        messages.success(request, 'فایل پروژه با موفقیت ایجاد و اپلود شد')
        return redirect('public:project_file__add')


class ProjectFileList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'public/project_file/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def sort(self, project_files):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            project_files = project_files.order_by('-id')
        elif sort_by == 'oldest':
            project_files = project_files.order_by('id')
        return project_files

    def filter(self, project_files):
        qs = self.request.GET
        search = qs.get('search', None)
        if search:
            project_files = project_files.filter(name__icontains=search)
        return project_files

    def get(self, request):
        project_files = models.ProjectFile.objects.all()
        project_files = self.filter(project_files)
        project_files = self.sort(project_files)
        pagination, project_files = self.pagination(project_files)
        context = {
            'pagination': pagination,
            'project_files': project_files,
            'projects': models.Project.objects.all()
        }
        return render(request, self.template_name, context)


class ProjectFileDetail(LoginRequiredMixin, View):
    template_name = 'public/project_file/detail.html'

    def get(self, request, project_file_id):
        project_file = get_object_or_404(models.ProjectFile, id=project_file_id)
        context = {
            'project_file': project_file,
            # permissions
            'has_perm_to_modify': project_file.has_perm_to_modify(request.user)
        }
        return render(request, self.template_name, context)


class ProjectFileDelete(LoginRequiredMixin, View):

    def get(self, request, project_file_id):
        project_file = get_object_or_404(models.ProjectFile, id=project_file_id)
        if not project_file.has_perm_to_modify(request.user):
            raise PermissionDenied
        project_file.delete()
        messages.success(request, 'فایل پروژه با موفقیت حذف شد')
        return redirect('public:project_file__list')
