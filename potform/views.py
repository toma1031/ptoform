from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.forms import AuthenticationForm
from .models import User, RequestPTO
from . import forms
from .forms import LoginForm, RequestPTOForm
from django.urls import reverse_lazy
from django.db.models import Q



class LoginView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"

# ここでURLの棲み分けをする, get_success_urlはLoginViewの関数の一種
    def get_success_url(self):
        user = User.objects.filter(username=self.request.POST['username'])[0]
        if user.is_employee:
            return reverse('employee')
        elif user.is_supervisor:
            return reverse('supervisor')
        else:
            return reverse('hr')
# LoginRequiredMixin, TemplateViewとすることで、テンプレートにはログインが必要ということになる
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class EmployeeView(LoginRequiredMixin, CreateView):
    model = RequestPTO
    form_class = RequestPTOForm
    template_name = "employee.html"
    success_url = reverse_lazy('success')

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_employee:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

    def form_valid(self, form):
        form = form.save(commit=False)
        form.post_employee = self.request.user
        form.save()
        return redirect('success')

class SupervisorView(LoginRequiredMixin, ListView):
    context_object_name = 'request_list'
    model = RequestPTO
    template_name = "supervisor.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_supervisor:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

    def post(self, request, *args, **kwargs):

# もしPOSTされたname="request"のvalue=Approveならば対象のPTOオブジェクトのrequestを1
        if  self.request.POST['request'] == 'Approve':
            queryset = RequestPTO.objects.filter(id=self.request.POST['id']).update(request=1)
        else:
            queryset = RequestPTO.objects.filter(id=self.request.POST['id']).update(request=2)
        return redirect('supervisor')

    def get_queryset(self):
        return RequestPTO.objects.filter(request=3,chose_supervisor=self.request.user)

class HrView(LoginRequiredMixin, ListView):
    context_object_name = 'request_list'
    model = RequestPTO
    queryset = RequestPTO.objects.filter(request=1)
    template_name = "hr.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_hr:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

    def post(self, request, *args, **kwargs):

        if  self.request.POST['request'] == 'Approve':
            queryset = RequestPTO.objects.filter(id=self.request.POST['id']).update(request=4)
        else:
            queryset = RequestPTO.objects.filter(id=self.request.POST['id']).update(request=2)
        return redirect('hr')

class ApprovedRequestView(LoginRequiredMixin, ListView):
    context_object_name = 'request_list'
    model = RequestPTO
    request = RequestPTO.objects.filter(request=4)
    template_name = "approved_request_hr.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_hr:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

class ApprovedRequestDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'request'
    model = RequestPTO
    request = RequestPTO.objects.filter(request=4)
    template_name = "approved_request_hr_detail.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_hr:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

class DeclinedRequestView(LoginRequiredMixin, ListView):
    context_object_name = 'request_list'
    model = RequestPTO
    request = RequestPTO.objects.filter(request=2)
    template_name = "declined_request_hr.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_hr:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

class DeclinedRequestDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'request'
    model = RequestPTO
    request = RequestPTO.objects.filter(Q(request=4) | Q(request=2))
    template_name = "declined_request_hr_detail.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_hr:
            return super().get(request, **kwargs)
        else:
            return redirect('index')


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "success.html"






