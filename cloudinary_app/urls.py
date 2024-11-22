from django.urls import path
from .views import home,ai_task

urlpatterns = [
    path('',home,name="home"),
    path('process/',ai_task,name="process"),
]
app_name="cloudinary"