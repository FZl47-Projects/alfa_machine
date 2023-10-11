from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout as logout_handler
from public.models import Department, Task
from .models import User
from account.auth.decorators import user_role_required_cbv


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


class SignUp(View):
    template_name = 'account/signup.html'
    def get(self, request):
         return render(request, self.template_name)
    def post(self, request):
        post = request.POST
        email = post.get('email', None)
        password = post.get('password', None)
        password2 = post.get('password2', None)
        if password != password2:
            messages.error(request, 'رمز های وارد شده یکسان نیستند')
            return redirect('account:signup')
        user = get_object_or_404(User, email= email)
        if user.password is None:
            user.set_password(password)
            user.save()
            return redirect ('account:login')
        messages.error(request,'کاربری با این مشخصات ثبت نام شده')
        return redirect('account:signup')
        

class NewUser(View):
    template_name = 'account/new_user.html'
    def get(self, request):
        context={
        'departments': Department.objects.all(),
        }
        return render(request, self.template_name, context)
    def post(self, request):
        post = request.POST
        email = post.get('email', None)
        first_name = post.get('first_name', None)
        role = post.get('role', None)
        department_id = post.get('department', None)
        department = Department.objects.get(id=department_id)
        if email and role and department and first_name:
            user = User(first_name=first_name, email= email, department= department, role= role)
            user.save()
        else:
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
        return redirect ('account:new_user')

class Logout(View):

    def get(self,request):
        logout_handler(request)
        return redirect('account:login')

class UserProfile(View):
    template_name = 'account/user_profile.html'
    @user_role_required_cbv(['super_user'])
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        context = {
            'user': user,
            'tasks': Task.objects.filter(allocator_user=user),
            'departments': Department.objects.all()
        }
        return render(request, self.template_name, context)
    def post(self, request, user_id):
        post = request.POST
        user = User.objects.get(id=user_id)
        print(user.first_name)
        user.email = post.get('email', None)
        user.first_name = post.get('name', None)
        user.role = post.get('role', None)
        department_id = post.get('department', None)
        user.department = Department.objects.get(id=department_id)
        user.save()
        return redirect ('departments.general:users_list')
