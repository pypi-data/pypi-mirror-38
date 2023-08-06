from django.db import models
from django.conf import settings
from django.utils import timezone




#Per page analytics
class pageAnalytics(models.Model):
	created = models.DateTimeField(auto_now = False, auto_now_add = True)
	os = models.CharField(max_length=40)
	browsers = models.CharField(max_length=40)
	languages = models.CharField(max_length=200)
	page = models.CharField(max_length=200)
	avg_load_time = models.FloatField()
	country = models.CharField(max_length=50,default='')
	

	def __str__(self):
		return str(self.page)


