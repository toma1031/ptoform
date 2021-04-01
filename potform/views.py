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
    paginate_by = 8
    template_name = "supervisor.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_supervisor:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

    def post(self, request, *args, **kwargs):

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
    paginate_by = 8

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
            queryset = RequestPTO.objects.filter(id=self.request.POST['id']).update(request=2, confirm_hr=self.request.user)
        return redirect('hr')

class ApprovedRequestView(LoginRequiredMixin, ListView):
    context_object_name = 'request_list'
    model = RequestPTO
    queryset = RequestPTO.objects.filter(request=4)
    template_name = "approved_request_hr.html"
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_hr:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

    def get_queryset(self):
        q_request_date_from = self.request.GET.get('query')
        
        if q_request_date_from:
            object_list = RequestPTO.objects.filter(
                Q(request_date_from__icontains=q_request_date_from))
        else:
            object_list = RequestPTO.objects.filter(request=4)
        return object_list.filter(request=4)

class ApprovedRequestDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'request'
    model = RequestPTO
    queryset = RequestPTO.objects.filter(request=4)
    template_name = "approved_request_hr_detail.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_hr:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

class EmployeeApprovedRequestView(LoginRequiredMixin, ListView):
    context_object_name = 'request_list'
    model = RequestPTO
    queryset = RequestPTO.objects.filter(request=4)
    paginate_by = 8
    template_name = "approved_request_employee.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_employee:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

    def get_queryset(self):
        # return RequestPTO.objects.filter(request=4,post_employee=self.request.user)

        q_request_date_from = self.request.GET.get('query')
        
        if q_request_date_from:
            object_list = RequestPTO.objects.filter(
                Q(request_date_from__icontains=q_request_date_from))
        else:
            object_list = RequestPTO.objects.filter(request=4, post_employee=self.request.user)
        return object_list.filter(request=4, post_employee=self.request.user)


class EmployeeApprovedRequestDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'request'
    model = RequestPTO
    queryset = RequestPTO.objects.filter(request=4)
    template_name = "approved_request_employee_detail.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_employee:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

class DeclinedRequestView(LoginRequiredMixin, ListView):
    context_object_name = 'request_list'
    model = RequestPTO
    queryset = RequestPTO.objects.filter(request=2)
    paginate_by = 8
    template_name = "declined_request_hr.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_hr:
            return super().get(request, **kwargs)
        else:
            return redirect('index')

    def get_queryset(self):
        q_request_date_from = self.request.GET.get('query')
        
        if q_request_date_from:
            object_list = RequestPTO.objects.filter(
                Q(request_date_from__icontains=q_request_date_from))
        else:
            object_list = RequestPTO.objects.filter(request=2)
        return object_list.filter(request=2)

class DeclinedRequestDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'request'
    model = RequestPTO
    queryset = RequestPTO.objects.filter(request=2)
    template_name = "declined_request_hr_detail.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_hr:
            return super().get(request, **kwargs)
        else:
            return redirect('index')


class EmployeeDeclinedRequestView(LoginRequiredMixin, ListView):
    context_object_name = 'request_list'
    model = RequestPTO
    queryset = RequestPTO.objects.filter(request=2)
    paginate_by = 8
    template_name = "declined_request_employee.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_employee:
            return super().get(request, **kwargs)
        else:
            return redirect('index')
    
    def get_queryset(self):
        # return RequestPTO.objects.filter(request=2,post_employee=self.request.user)

        q_request_date_from = self.request.GET.get('query')
        
        if q_request_date_from:
            object_list = RequestPTO.objects.filter(
                Q(request_date_from__icontains=q_request_date_from))
        else:
            object_list = RequestPTO.objects.filter(request=2, post_employee=self.request.user)
        return object_list.filter(request=2, post_employee=self.request.user)

class EmployeeDeclinedRequestDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'request'
    model = RequestPTO
    queryset = RequestPTO.objects.filter(request=2)
    template_name = "declined_request_employee_detail.html"

    def get(self, request, *args, **kwargs):
        user =  User.objects.filter(username=self.request.user)
        if user and user[0].is_employee:
            return super().get(request, **kwargs)
        else:
            return redirect('index')
    
    def post(self, request, *args, **kwargs):
        if  self.request.POST['request'] == 'Resubmit':
            queryset = RequestPTO.objects.filter(id=self.request.POST['id']).update(request=3)
            print(self.request.POST)
        return redirect('success')

class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "success.html"






