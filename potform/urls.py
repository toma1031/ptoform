from django.urls import path
from potform import views
from .views import IndexView, EmployeeView, SupervisorView, HrView, SuccessView, LoginView

urlpatterns = [
    path('', IndexView.as_view()),
    # ここから追記
    path('employee/', EmployeeView.as_view(), name='employee'),
    path('supervisor/', SupervisorView.as_view(), name='supervisor'),
    path('hr/', HrView.as_view(), name='hr'),
    path('success/', SuccessView.as_view(), name='success'),
    path('login/', LoginView.as_view(), name='login')
]