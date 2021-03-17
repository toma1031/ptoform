from django.contrib.auth.forms import AuthenticationForm
from .models import (RequestPTO, get_user_model)
from django import forms

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)


class RequestPTOForm(forms.ModelForm):
  chose_supervisor = forms.ModelChoiceField(
                          queryset=get_user_model().objects.filter(is_supervisor=True),
                          widget=forms.Select)

  request_date_from = forms.DateField(
                          widget=forms.DateInput(attrs={"type":"date"}),
                          input_formats=['%Y-%m-%d'])

  request_date_to = forms.DateField(
                          widget=forms.DateInput(attrs={"type":"date"}),
                          input_formats=['%Y-%m-%d'])

  note = forms.Textarea()

  # request = forms.

  class Meta:
    model = RequestPTO
    fields = ('chose_supervisor', 'request_date_from', 'request_date_to', 'note')




