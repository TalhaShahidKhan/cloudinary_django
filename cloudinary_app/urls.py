from django.urls import path
from .views import home,ai_task,ai_upscale,enhance,bgremove,genfill,genreplace


htmx_urlpatterns = [
    path('upscale/<str:pID>/',ai_upscale,name="ups"),
    path('enhance/<str:pID>/',enhance,name="enhance"),
    path('fill/<str:pID>/',genfill,name="fill"),
    path('replace/<str:pID>/',genreplace,name="replace"),
    path('bggrmv/<str:pID>/',bgremove,name="bgrmv"),
]


urlpatterns = [
    path('',home,name="home"),
    path('process/<str:img_id>/',ai_task,name="process"),
]


urlpatterns+=htmx_urlpatterns
app_name="cloudinary"