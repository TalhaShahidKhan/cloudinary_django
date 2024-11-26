from django.urls import path
from .views import home,ai_task,ai_upscale,enhance,bgremove,genfill,genreplace,limited_view




urlpatterns = [
    path('test/',limited_view,name="test"),


    path('',home,name="home"),
    path('process/<str:img_id>/',ai_task,name="process"),
    path('upscale/<str:pID>/',ai_upscale,name="ups"),
    path('enhance/<str:pID>/',enhance,name="enhance"),
    path('fill/<str:pID>/',genfill,name="fill"),
    path('replace/<str:pID>/',genreplace,name="replace"),
    path('bggrmv/<str:pID>/',bgremove,name="bgrmv"),
]


app_name="cloudinary"