from django.contrib import messages
from django.views.generic import View
from django.shortcuts import redirect
from core.utils import form_validate_err
from notification.models import NotificationDepartment
from . import forms


class TicketDepartment(View):

    def post(self, request):
        referer_url = request.META.get('HTTP_REFERER',None )

        data = request.POST.copy()
        # set default values
        data['from_department'] = request.user.department
        f = forms.TicketDepartmentForm(data, request.FILES)
        if form_validate_err(request, f) is False:
            return redirect(referer_url or '/error')
        ticket_obj = f.save()
        NotificationDepartment.objects.create(
            title='درخواست از واحد',
            priority=1,
            description=ticket_obj.description,
            project=ticket_obj.project,
            file=ticket_obj.file,
            from_department=ticket_obj.from_department,
            to_department=ticket_obj.to_department,
        )
        messages.success(request,'عملیات مورد نظر با موفقیت انجام شد')
        return redirect(referer_url or '/success')