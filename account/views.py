from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from public.models import Department
from .auth.decorators import user_role_required_cbv
from .models import User
from . import forms


class Login(View):
    template_name = 'account/login.html'

    def get(self, request):
        return render(request, self.template_name)

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


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('account:login')


class ResetPassword(View):

    def get(self, request):
        pass


class UserAdd(LoginRequiredMixin, View):
    template_name = 'account/user/add.html'

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request):
        context = {
            'departments': Department.objects.all()
        }
        return render(request, self.template_name, context)

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def post(self, request):
        data = request.POST

        # check unique email
        user = User.objects.filter(email=data.get('email')).first()
        if user:
            messages.error(request, 'ایمیل وارد شده تکراری میباشد')
            return redirect('account:user__add')

        f = forms.UserCreate(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('account:user__add')
        user = f.save(commit=False)
        user.set_password(f.cleaned_data['password2'])
        user.save()
        messages.success(request, 'کاربر با موفقیت ایجاد شد')
        return redirect('account:user__add')


class UserList(LoginRequiredMixin, View):
    pagination_count = 25
    template_name = 'account/user/list.html'

    def pagination(self, objects):
        paginator = Paginator(objects, self.pagination_count)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return page_obj, page_obj.object_list

    def filter(self, users):
        qs = self.request.GET
        search = qs.get('search', None)
        department = qs.get('department', 'all')
        if search:
            users = users.filter(email__icontains=search)
        if (department != 'all') and (department.isdigit()):
            users = users.filter(department_id=department)
        return users

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request):
        users = User.objects.all()
        users = self.filter(users)
        pagination, users = self.pagination(users)
        context = {
            'pagination': pagination,
            'users': users,
            'departments': Department.objects.all()
        }
        return render(request, self.template_name, context)


class UserDetail(LoginRequiredMixin, View):
    template_name = 'account/user/detail.html'

    @user_role_required_cbv(['super_user', 'control_project_user'])
    def get(self, request, user_id):
        user_obj = get_object_or_404(User, id=user_id)
        context = {
            'user': user_obj,
            'departments': Department.objects.all(),
            # permissions
            'has_perm_to_modify': user_obj.has_perm_to_modify(request.user)
        }
        return render(request, self.template_name, context)


class UserDelete(LoginRequiredMixin, View):
    template_name = 'account/user/detail.html'

    def get(self, request, user_id):
        if not User.has_perm_to_modify(request.user):
            raise PermissionDenied
        user_obj = get_object_or_404(User, id=user_id)
        user_obj.delete()
        messages.success(request, 'کاربر با موفقیت حذف شد')
        return redirect('account:user__list')


class UserUpdate(LoginRequiredMixin, View):
    template_name = 'account/user/detail.html'

    def post(self, request, user_id):
        if not User.has_perm_to_modify(request.user):
            raise PermissionDenied
        user_obj = get_object_or_404(User, id=user_id)
        data = request.POST
        f = forms.UserUpdate(data, instance=user_obj)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی پر نمایید')
            return redirect(user_obj.get_absolute_url())
        f.save()
        messages.success(request, 'کاربر با موفقیت بروزرسانی شد')
        return redirect(user_obj.get_absolute_url())


class UserProfileDetail(LoginRequiredMixin, View):
    # TODO: should be completed
    template_name = 'account/user/profile.html'

    def get(self, request):
        context = {
            'user': request.user,
        }
        return render(request, self.template_name, context)


# ----

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
        user = get_object_or_404(User, email=email)
        if user.password is None:
            user.set_password(password)
            user.save()
            return redirect('account:login')
        messages.error(request, 'کاربری با این مشخصات ثبت نام شده')
        return redirect('account:signup')


class NewUser(View):
    template_name = 'account/new_user.html'

    def get(self, request):
        context = {
            'departments': Department.objects.all(),
            'roles': User.ROLE_USER_OPTIONS
        }
        return render(request, self.template_name, context)

    def post(self, request):
        data = request.POST
        f = forms.CreateUserForm(data)
        if not f.is_valid():
            messages.error(request, 'لطفا فیلد هارا به درستی وارد نمایید')
            return redirect('account:new_user')
        user = f.save(commit=False)
        user.set_password(f.cleaned_data['password'])
        user.save()
        messages.success(request, 'کاربر با موفقیت ایجاد شد')
        return redirect('account:new_user')


# class UserProfile(View):
#     template_name = 'account/user_profile.html'
#
#     @user_role_required_cbv(['super_user'])
#     def get(self, request, user_id):
#         user = get_object_or_404(User, id=user_id)
#         context = {
#             'user': user,
#             'tasks': Task.objects.filter(allocator_user=user),
#             'departments': Department.objects.all()
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request, user_id):
#         post = request.POST
#         user = User.objects.get(id=user_id)
#         user.email = post.get('email', None)
#         user.first_name = post.get('name', None)
#         user.role = post.get('role', None)
#         department_id = post.get('department', None)
#         user.department = Department.objects.get(id=department_id)
#         user.save()
#         return redirect('departments.general:users_list')
