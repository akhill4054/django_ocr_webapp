from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^$|^home$|^upload$', views.home, name='upload'),
    path('upload/process/', views.upload_and_process, name='upload_and_process'),
    path(r'result/<str:file_id>/<str:file_name>/', views.result, name='result'),
]