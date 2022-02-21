from django.urls import path

from . import views

urlpatterns = [
    path('', views.getdatafrominter, name='getdatafrominter'),
    path('getleavedate', views.getLeaveDate, name='getleavedate'),
]
