from django.urls import path
from . import views

app_name = 'animation'

urlpatterns = [
    path('', views.index, name='index'),
    path('start_pose_estimation/', views.start_pose_estimation, name='start_pose_estimation'),
    path('show_motion/', views.show_motion, name='show_motion'),
]
