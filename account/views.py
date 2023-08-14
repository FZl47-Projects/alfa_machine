from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate, login


class Login(View):
    template_name = 'account/login.html'

    def get(self, request):
        return render(request,self.template_name)

    def post(self, request):
        data = request.POST
        email = data.get('email', None)
        password = data.get('password', None)
        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is None:
                messages.error(request, 'کاربری با این مشخصات یافت نشد')
                return redirect('account:login')
            login(request, user)
            messages.success(request, 'خوش امدید')
            # redirect by role user to panel
            # return redirect('public:home')
        else:
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
        return redirect('account:login')
