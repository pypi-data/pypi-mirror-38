import subprocess
import itertools
import datetime
import requests
import json

def requestCheck(request):
	"""
	https://developer.mozilla.org/en-US/docs/Web/HTTP/Browser_detection_using_the_user_agent
	from the request received for connection
	"""
	data = {}
	data['browser'] = ""
	data['os'] = ""
	data['languages'] = []

	#Get Supported Languages
	LanguageItems = request.META['HTTP_ACCEPT_LANGUAGE'].split(",")

	for item in LanguageItems:
		languages=item.split(";")
		data['languages'].append(languages[0].strip())


	if request.META['HTTP_USER_AGENT'].lower().find('linux')>=0:
		data['os'] = 'Linux'
	elif request.META['HTTP_USER_AGENT'].lower().find('windows')>=0:
		data['os'] = "Windows"
	elif request.META['HTTP_USER_AGENT'].lower().find('macintosh')>=0:
		data['os'] = "Macintosh"

	FindFirefox = request.META['HTTP_USER_AGENT'].find('Firefox/')
	FindSeamonkey = request.META['HTTP_USER_AGENT'].find('Seamonkey/')
	FindChrome = request.META['HTTP_USER_AGENT'].find('Chrome/')
	FindChromium = request.META['HTTP_USER_AGENT'].find('Chromium/')
	FindSafari = request.META['HTTP_USER_AGENT'].find('Safari/')
	FindOpera  = request.META['HTTP_USER_AGENT'].find('Opera/') or request.META['HTTP_USER_AGENT'].find('OPR/')
	FindIE = request.META['HTTP_USER_AGENT'].find('MSIE')

	#check for firefox
	if FindFirefox > 0	and FindSeamonkey ==-1:
		data['browser'] = "firefox"
	#check for  Seamonkey
	elif FindFirefox ==-1 and FindSeamonkey > 0:
		data['browser'] = "seamonkey"
	elif FindChromium > 0:
		data['browser'] = "chromium"
	elif FindSafari > 0 and FindChrome ==-1 and FindChromium ==-1:
		data['browser'] = "safari"
	elif FindChrome > 0 and FindChromium ==-1:
		data['browser'] = "chrome"
	elif FindIE > 0:
		data['browser'] = "ie"
	else:
		data['browser'] = "others"

	return data


def timeDuration(fmt):
	duration = ""
	print ("current time:",datetime.datetime.now())
	if fmt == "hours":
		duration = datetime.datetime.today() - datetime.timedelta(hours = 24)
	elif fmt == "days":
		duration = datetime.datetime.today() - datetime.timedelta(days = 30)
	elif fmt == "minutes":
		duration = datetime.datetime.today() - datetime.timedelta(minutes = 60)
	return duration



def ipInfo(ip):
	#curl ipinfo.io/8.8.4.4
	r = requests.get("http://ipinfo.io/"+ip)
	if r.status_code == 200:
		jsondata = json.loads(r.text)
		return jsondata
