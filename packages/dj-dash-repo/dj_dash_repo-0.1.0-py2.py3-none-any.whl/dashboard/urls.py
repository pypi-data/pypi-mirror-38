from django.contrib import admin
from django.urls import path,include,re_path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('',views.index),
    path('all/',views.getInfo),
    path('all/<int:fmt>',views.getInfo),
]
