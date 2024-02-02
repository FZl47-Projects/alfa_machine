from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from public.models import Project, Department
from notification.utils import create_notification_by_role
from account.auth.decorators import user_role_required_cbv
from . import models, forms


class Index(View):
    template_name = 'warehouse/index.html'

    @user_role_required_cbv(['warehouse_user'])
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


class ItemAdd(LoginRequiredMixin, View):
    template_name = 'warehouse/item/add.html'

    @user_role_required_cbv(['warehouse_user', 'control_project_user', 'super_user'])
    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        f = forms.ItemWarehouseCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('dp_warehouse:item__add')
        item = f.save()
        messages.success(request, 'ایتم انبار با موفقیت ثبت شد')
        create_notification_by_role(
            'ثبت ایتم انبار جدید',
            description='ایجاد به صورت خودکار',
            from_department=request.user.department,
            to_users=('warehouse_user', 'super_user', 'control_project_user'),
            projects=(item.project,),
            attached_link=item.get_absolute_url()
        )
        return redirect(item.get_absolute_url())


class ItemList(LoginRequiredMixin, View):
    template_name = 'warehouse/item/list.html'
    pagination_count = 25

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def sort(self, tasks):
        sort_by = self.request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            tasks = tasks.order_by('-id')
        elif sort_by == 'oldest':
            tasks = tasks.order_by('id')
        return tasks

    def filter(self, items):
        qs = self.request.GET
        search = qs.get('search', None)
        project = qs.get('project', 'all')

        if search:
            items = items.filter(name__icontains=search)

        if (project != 'all') and (project.isdigit()):
            items = items.filter(project_id=project)

        return items

    @user_role_required_cbv(['warehouse_user', 'control_project_user', 'super_user', 'commerce_user', 'financial_user'])
    def get(self, request):
        items = models.ItemWarehouse.objects.all()
        items = self.filter(items)
        items = self.sort(items)
        pagination, items = self.pagination(items)
        context = {
            'pagination': pagination,
            'items': items,
            'projects': Project.objects.filter(is_active=True)
        }

        return render(request, self.template_name, context)


class ItemDetail(LoginRequiredMixin, View):
    template_name = 'warehouse/item/detail.html'

    @user_role_required_cbv(['warehouse_user', 'control_project_user', 'super_user', 'commerce_user', 'financial_user'])
    def get(self, request, item_id):
        item = get_object_or_404(models.ItemWarehouse, id=item_id)
        context = {
            'item': item,
            'files': item.get_files(),
            'projects': Project.objects.filter(is_active=True),
            # permissions
            'has_perm_to_modify': item.has_perm_to_modify(request.user)
        }
        return render(request, self.template_name, context)


class ItemDelete(LoginRequiredMixin, View):

    def get(self, request, item_id):
        if not models.ItemWarehouse.has_perm_to_modify(request.user):
            raise PermissionDenied
        item = get_object_or_404(models.ItemWarehouse, id=item_id)
        item.delete()
        messages.success(request, 'ایتم انبار با موفقیت حذف شد')
        return redirect('dp_warehouse:item__list')


class ItemUpdate(LoginRequiredMixin, View):

    def post(self, request, item_id):
        if not models.ItemWarehouse.has_perm_to_modify(request.user):
            raise PermissionDenied
        item = get_object_or_404(models.ItemWarehouse, id=item_id)
        f = forms.ItemWarehouseUpdate(request.POST, instance=item)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(item.get_absolute_url())
        f.save()
        messages.success(request, 'ایتم انبار با موفقیت بروزرسانی شد')
        return redirect(item.get_absolute_url())


class ItemFileAdd(LoginRequiredMixin, View):

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER')
        data = request.POST.copy()
        # set additional values
        data['from_department'] = request.user.department
        f = forms.ItemWarehouseFileCreate(data, files=request.FILES)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(referer_url)
        item_file = f.save()
        return redirect(item_file.register_warehouse.get_absolute_url())


class ItemFileDelete(LoginRequiredMixin, View):

    def get(self, request, item_file_id):
        referer_url = request.META.get('HTTP_REFERER')
        item_file = get_object_or_404(models.ItemFile, id=item_file_id, from_department=request.user.department)
        item_file.delete()
        messages.success(request, 'فایل پیوست ایتم انبار با موفقیت حذف شد')
        return redirect(referer_url)
