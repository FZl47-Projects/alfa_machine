from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout as logout_handler


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
            if user.department is None:
                messages.error(request, 'برای این کاربر واحدی ثبت نشده است لطفا به پشتیبانی اطلاع دهید')
                return redirect('account:login')
            login(request, user)
            messages.success(request, 'خوش امدید')
            return redirect('public:index')
        else:
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
        return redirect('account:login')


def logout(request):
    logout_handler(request)
    return redirect('account:login')