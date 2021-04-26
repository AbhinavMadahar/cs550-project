from django.urls import path

from . import views
app_name = "server"

urlpatterns= [
    path(r'recommendation', views.index , name="index")
]