from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Q
from core.utils import form_validate_err
from public.models import Project
from account.auth.decorators import user_role_required_cbv
from . import models, forms


class Index(View):
    template_name = 'warehouse/index.html'

    @user_role_required_cbv(['warehouse_user', 'control_project_user', 'super_user'])
    def get(self, request):
        projects = Project.objects.filter(is_active=True)

        context = {
            'tickets': request.user.get_tickets(),
            'notifications': request.user.department.get_notifications(),
            'projects': projects,
            'ongoing_projects': projects.filter(status__in=['checking', 'paused', 'under_construction'])[:4],
        }
        return render(request, self.template_name, context)


class Registration(View):
    template_name = 'warehouse/registrations_list.html'

    def search(self, request, items):
        search = request.GET.get('search', None)
        if not search:
            return items
        if search.isdigit():
            lookup = Q(code=search)
            items = items.filter(lookup)
        else:
            lookup = Q(name__icontains=search) | Q(size=search) | Q(receiver__icontains=search)
            items = items.filter(lookup)
        return items

    def sort(self, request, items):
        sort_by = request.GET.get('sort_by', 'latest')
        if sort_by == 'latest':
            items = items.order_by('-id')
        elif sort_by == 'oldest':
            items = items.order_by('id')
        return items

    @user_role_required_cbv(['warehouse_user', 'control_project_user', 'super_user', 'commerce_user', 'financial_user'])
    def get(self, request):
        items = models.WarehouseRegistration.objects.all()
        items = self.search(request, items)
        items = self.sort(request, items)

        context = {
            'items': items,
            'projects': Project.objects.filter(is_active=True)
        }

        return render(request, self.template_name, context)

    @user_role_required_cbv(['warehouse_user', 'control_project_user', 'super_user', 'commerce_user', 'financial_user'])
    def post(self, request):
        data = request.POST

        f = forms.WarehouseRegistrationForm(data, files=request.FILES)
        if form_validate_err(request, f) is False:
            return redirect('dp_warehouse:registration')
        f.save()

        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect('dp_warehouse:registration')


class RegisterDetail(View):

    @user_role_required_cbv(['warehouse_user', 'control_project_user', 'super_user', 'commerce_user', 'financial_user'])
    def post(self, request, item_id):
        referer_url = request.META.get('HTTP_REFERER', None)

        data = request.POST
        item_obj = models.WarehouseRegistration.objects.get(id=item_id)

        f = forms.WarehouseRegistrationForm(data, instance=item_obj, files=request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()

        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(referer_url or '/success')
