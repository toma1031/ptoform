from django.urls import path
from potform import views
from .views import (IndexView, EmployeeView, SupervisorView, HrView, SuccessView, LoginView, ApprovedRequestView, DeclinedRequestView, ApprovedRequestDetailView, DeclinedRequestDetailView)

urlpatterns = [
    path('', IndexView.as_view()),
    path('employee/', EmployeeView.as_view(), name='employee'),
    path('supervisor/', SupervisorView.as_view(), name='supervisor'),
    path('hr/', HrView.as_view(), name='hr'),
    path('success/', SuccessView.as_view(), name='success'),
    path('login/', LoginView.as_view(), name='login'),
    path('approved_request_hr/', ApprovedRequestView.as_view(), name='approved_request_hr'),
    path('declined_request_hr/', DeclinedRequestView.as_view(), name='declined_request_hr'),
    path('approved_request_hr_detail/<int:pk>/', ApprovedRequestDetailView.as_view(), name='approved_request_hr_detail'),
    path('declined_request_hr_detail/<int:pk>/', DeclinedRequestDetailView.as_view(), name='declined_request_hr_detail'),

]