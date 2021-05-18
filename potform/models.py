
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class User(AbstractUser):
  is_employee = models.BooleanField(default=False)
  is_supervisor = models.BooleanField(default=False)
  is_hr = models.BooleanField(default=False)

class RequestPTO(models.Model):
  post_employee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name ='post_employee')
  chose_supervisor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name ='chose_supervisor')
  confirm_hr = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name ='confirm_hr')
  request_date_from = models.DateTimeField(null=False)
  request_date_to = models.DateTimeField(null=False)
  note = models.TextField(null=True, blank=True, max_length=200)
  request = models.IntegerField(default=3)

  def __str__(self):
    return str(self.request_date_from)