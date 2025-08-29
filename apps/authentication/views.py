from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from apps.authentication.forms import LoginForm
from apps.common.utils.decorators import not_logged_in
from apps.common.utils.notify import Notify


# Create your views here.

notify = Notify()


@method_decorator(not_logged_in, name="dispatch")
class LoginView(View):
    form_class = LoginForm
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'authentication/login.html',{
                'form': self.form_class,
            }
        )
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            login(request, member)
            return redirect('management:core:dashboard')
        else:
            for error_list in form.errors.values():
                for error in error_list:
                    notify.notify(request=request,message=error, level='error')
        return redirect('authentication:login')


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('authentication:login')


@method_decorator(login_required, name="dispatch")
class PermissionDeniedView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'authentication/permission-denied.html'
        )