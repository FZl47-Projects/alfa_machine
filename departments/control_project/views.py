from django.shortcuts import render
from django.views.generic import View


class Index(View):
    # TODO: should be complete
    template_name = ''

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass
