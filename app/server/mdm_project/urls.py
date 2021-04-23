from django.urls import path

from . import views
app_name = "mdm_project"

urlpatterns= [
    path('', views.index , name="index")
]