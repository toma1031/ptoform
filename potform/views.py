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
        form.confirm_hr = User.objects.filter(is_hr=True)[0]
        form.save()
        form.chose_supervisor.email_user(
                'PTO Request', 
                'New Request Recieved. Please login to PTO Form and check the Request!')
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
            queryset = RequestPTO.objects.filter(id=self.request.POST['id'])
            queryset.update(request=1)
            queryset[0].confirm_hr.email_user(
                'PTO Request', 
                'New Request Recieved. Please login PTO Form and check the Request!')
        else:
            queryset = RequestPTO.objects.filter(id=self.request.POST['id'])
            queryset.update(request=2)
            queryset[0].post_employee.email_user(
                'Declined your PTO Request.', 
                'Declined your Request. Please login to PTO Form and resubmit or send new request.')
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
            queryset = RequestPTO.objects.filter(id=self.request.POST['id'])
            queryset.update(request=4)
            queryset[0].post_employee.email_user(
                'Approved your PTO Request!', 
                'Congratulation! Your request is approved!')
        else:
            queryset = RequestPTO.objects.filter(id=self.request.POST['id'])
            queryset.update(request=2, confirm_hr=self.request.user)
            queryset[0].post_employee.email_use(
                'Declined your PTO Request.', 
                'Declined your Request. Please login to PTO Form and resubmit or send new request.')
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

# Get関数はユーザーをそのViewにアクセスさせるか、させないかのフィルタリングに使用する
    def get(self, request, *args, **kwargs):
      # ユーザー変数にログインしているユーザーのユーザーネームを代入
        user =  User.objects.filter(username=self.request.user)
        # ユーザーがemployeeの場合
        if user and user[0].is_employee:
          # ページにアクセスさせる
          # super()はUpdateView。
          # 親クラスは継承元のことを言うのでPostUpdateViewのことでは無い。
          # requestにはurlなどの情報が入っている。
          # アクセス先のurlやメタ情報など様々な情報が含まれている。
          # kwargsにはアクセス時に送信されたキーワード引数が含まれる。
            return super().get(request, **kwargs)
        else:
          # その他はトップページに飛ばす
            return redirect('index')
    # def get_querysetはリストオブジェクトにフィルタリングをかける時に使用できる
    def get_queryset(self):
        # q_request_date_from変数に入力値（ここでは日付）を取得したものを代入
        q_request_date_from = self.request.GET.get('query')
        
        # q_request_date_from変数がある場合、すなわち入力値になにか入力されていた場合
        if q_request_date_from:
            # filter()で絞り込みをおこなっています。OR条件でクエリセットを取得するためにQオブジェクトを利用、Qオブジェクトを利用はSQLのor条件を実現するものです。
            # ここではrequest_date_fromに対して「__icontains」を付与することによって、q_request_date_fromの値を含む部分一致の検索を実現し、そのフィルタリングされたRequestPTOをobject_listに代入
            object_list = RequestPTO.objects.filter(
                Q(request_date_from__icontains=q_request_date_from))
        else:
            # q_request_date_from変数がない場合、すなわち入力値になにも入力されていない場合、
            # RequestPTOのクエリが４のもので、employeeでログインしているユーザー自身のRequestPTOをobject_listに代入
            object_list = RequestPTO.objects.filter(request=4, post_employee=self.request.user)
        # 最後にRequestPTOのクエリが４のもので、employeeでログインしているユーザー自身のobject_list、
        # すなわちRequestPTOを返す
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






