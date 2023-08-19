from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from core.utils import form_validate_err
from public.models import Project
from account.auth.decorators import user_role_required_cbv
from . import models, forms


class Index(View):
    template_name = 'warehouse/index.html'

    @user_role_required_cbv(['warehouse_user'])
    def get(self, request):
        context = {
            'items': models.MaterialItem.objects.filter(materialquality=None),
            'projects': Project.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)


class Items(View):
    template_name = 'warehouse/items.html'

    @user_role_required_cbv(['warehouse_user'])
    def get(self, request):
        context = {
            'items': models.MaterialItem.objects.all(),
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['warehouse_user'])
    def post(self, request):
        data = request.POST
        items = models.MaterialItem.objects.all()
        for item in items:
            item_checked = data.get(f'item-{item.id}', None)
            item.is_checked = True if item_checked == 'on' else False
            item.save()
        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect('dp_warehouse:items')


class Registration(View):
    template_name = 'warehouse/registration.html'

    @user_role_required_cbv(['warehouse_user'])
    def get(self, request):
        context = {
            'items': models.MaterialItem.objects.all(),
            'projects': Project.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['warehouse_user'])
    def post(self, request):
        data = request.POST
        f = forms.ItemRegisterForm(data)
        if form_validate_err(request, f) is False:
            return redirect('dp_warehouse:registration')
        f.save()
        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect('dp_warehouse:registration')


class RegisterDetail(View):

    @user_role_required_cbv(['warehouse_user'])
    def post(self, request, item_id):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST
        item_obj = models.MaterialItem.objects.get(id=item_id)
        f = forms.ItemRegisterUpdateForm(data, instance=item_obj)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class ItemsQualityPass(View):

    @user_role_required_cbv(['warehouse_user'])
    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST.copy()
        # set default values
        items = models.MaterialItem.objects.filter(materialquality=None).values_list('id', flat=True)
        items = list(items)
        data.setlist('items', items)
        f = forms.ItemsQualityPassForm(data)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class ItemsAllocationProject(View):
    template_name = 'warehouse/allocation-materials.html'

    @user_role_required_cbv(['warehouse_user'])
    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True),
            'items': models.MaterialItem.objects.all()
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['warehouse_user'])
    def post(self, request):
        data = request.POST
        items = models.MaterialItem.objects.all()
        project_id = data.get('project', 0)
        project_obj = Project.objects.get(id=project_id)
        items_selected = []
        for item in items:
            task_data_allocate = data.get(f'item-{item.id}', None)
            if task_data_allocate:
                items_selected.append(item)
        material_project = getattr(project_obj, 'materialproject', None)
        if material_project is None:
            material_project = models.MaterialProject.objects.create(
                project=project_obj)
        material_project.items.set(items_selected, clear=True)
        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect('dp_warehouse:items_allocation_project')
