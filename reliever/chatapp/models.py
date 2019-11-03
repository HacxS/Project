from django.db import models
from django.utils import timezone

# Create your models here.
class ChatSave(models.Model):
	from_user = models.CharField(max_length=50)
	to_user = models.CharField(max_length=50)
	message = models.CharField(max_length=1000)
	is_doctor = models.BooleanField(default=False)
	current_time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.from_user+'->'+self.to_user