from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from core.utils import form_validate_err
from public.models import Project
from . import models, forms


class Index(View):
    template_name = 'financial/index.html'

    def get(self, request):
        context = {
            'projects': Project.objects.filter(is_active=True)
        }
        return render(request, self.template_name, context)


class Payment(View):

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST
        f = forms.PaymentForm(data)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class PrePayment(View):

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER', None)
        data = request.POST
        f = forms.PrePaymentForm(data)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        f.save()
        messages.success(request, 'عملیات با موفقیت انجام شد')
        return redirect(referer_url or '/success')


class PaymentProject(View):
    template_name = 'financial/list.html'

    def get(self, request, project_id):
        project_obj = Project.objects.get(id=project_id)
        context = {
            'project': project_obj
        }
        return render(request, self.template_name, context)
