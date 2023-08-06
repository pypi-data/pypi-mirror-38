from django.shortcuts import render
from django.http import HttpResponse
import sys
import os
import itertools
from dashboard.utility import helper
from django.http import JsonResponse
from dashboard import models
from django.db.models import Count,Avg

from datetime import datetime

# Create your views here.

def index(request):
	return render(request,'dashboard/index.html')

def getInfo(request,fmt=1):
	website_hits = len(models.pageAnalytics.objects.all())
	if website_hits == 0:
		return JsonResponse({})
	data = {}
	#website hits
	data['hits'] = website_hits
	data['os'] = []
	data['languages'] = []
	data['browsers'] = []
	data['avg_load_time'] = []
	data['visits'] = []
	data['country'] = []

	#visits, per hours
	intFmt = {1:"minutes",2:"hours",3:"days"}
	duration=helper.timeDuration(intFmt[fmt])

	jobs = models.pageAnalytics.objects.filter(created__gte=duration).values('created')
	#print ("jobs",jobs)
	fmtMapping = {'days':"%Y %m %d",'hours':'%Y %m %d %H','minutes':"%Y %m %d %H %M"}
	grouped = itertools.groupby(jobs, lambda record: record.get("created").strftime(fmtMapping[intFmt[fmt]]))
	jobs_by_duration = [(day, len(list(jobs_this_day))) for day, jobs_this_day in grouped]

	for item in  jobs_by_duration:
		if intFmt[fmt] == "minutes":
			datetime_object = datetime.strptime(item[0], '%Y %m %d %H %M')
			data['visits'].append({'time':datetime_object.strftime("%H:%M"),'count':item[1]})
		elif intFmt[fmt] == "days":
			datetime_object = datetime.strptime(item[0], "%Y %m %d")
			data['visits'].append({'time':datetime_object.strftime("%d %b"),'count':item[1]})
		elif intFmt[fmt] == "hours":
			datetime_object = datetime.strptime(item[0], '%Y %m %d %H')
			data['visits'].append({'time':datetime_object.strftime("%H:00 %p"),'count':item[1]})


	#country details
	d = models.pageAnalytics.objects.values('country').annotate(count=Count('country'))
	for i in d:
		#print (key.os,value.os)
		if i['country']:
			data['country'].append(i)

	#os details
	d = models.pageAnalytics.objects.values('os').annotate(count=Count('os'))
	for i in d:
		#print (key.os,value.os)
		data['os'].append(i)

	#browsers details
	d = models.pageAnalytics.objects.values('browsers').annotate(count=Count('browsers'))
	for i in d:
		#print (key.os,value.os)
		data['browsers'].append(i)

	#os details
	languages = {}
	d = models.pageAnalytics.objects.values('languages').annotate(count=Count('languages'))

	for i in d:
		for k in eval(i['languages']):
			if k in languages.keys():
				languages[k]+=i['count']
			else:
				languages[k]=i['count']

	#data['languages'] = languages
	for item in languages:
		data['languages'].append({'languages':item,'count':languages[item]})

	#average_load_time
	d = models.pageAnalytics.objects.values('page').annotate(avg=Avg('avg_load_time'))
	for i in d:
		data['avg_load_time'].append(i)
	return JsonResponse(data)

