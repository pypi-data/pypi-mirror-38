import re
from django.db import connection
from time import time
from operator import add
from dashboard import models
from dashboard.utility import helper
from functools import reduce



class SimpleMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.python_time = 0
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # get number of db queries before we do anything
        n = len(connection.queries)

        # time the view
        self.start = time()
        # the view is called
        response = self.get_response(request)

        # Code to be executed for each request/response after

        self.total_time = time() - self.start

        # compute the db time for the queries just run
        self.db_queries = len(connection.queries) - n
        if self.db_queries:
            self.db_time = reduce(add, [float(q['time'])
                                   for q in connection.queries[n:]])
        else:
            self.db_time = 0.0

        # and backout python time
        self.python_time = self.total_time - self.db_time

        self.stats = {
            'total_time': self.total_time,
            'python_time': self.python_time,
            'db_time': self.db_time,
            'db_queries': self.db_queries,
        }

        if request.get_full_path().lower().find('admin') == -1 and request.get_full_path().lower().find('analytics') == -1:
            self.updateDb(request)
        return response

    def updateDb(self,request):
        data = helper.requestCheck(request)
        addData = helper.ipInfo(request.META['REMOTE_ADDR'])
        if "country" in addData.keys():
            data['country'] = addData["country"]
        else:
            data['country'] = ""


        #data['country'] = helper.ipInfo(request.META['REMOTE_ADDR'])
        # if models.pageAnalytics.objects.all().filter(page=request.get_full_path()):
        #     urldata = models.pageAnalytics.objects.all().filter(page=request.get_full_path())
        #     hits= urldata[0].hits_on_page +1
        #     models.pageAnalytics.objects.all().filter(page=request.get_full_path()).update(os=data['os'],browsers=data['browser'],languages=str(data['languages']),page=request.get_full_path(),avg_load_time=self.python_time,hits_on_page=hits)
        # else:
        #     p = models.pageAnalytics(os=data['os'],browsers=data['browser'],languages=str(data['languages']),page=request.get_full_path(),avg_load_time=self.python_time)
        #     p.save()
        p = models.pageAnalytics(os=data['os'],browsers=data['browser'],languages=str(data['languages']),page=request.get_full_path(),avg_load_time=self.python_time,country=data['country'])
        p.save()
