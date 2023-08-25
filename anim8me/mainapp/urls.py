from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('webcam/', views.webcam_view, name='webcam'),
    path('webcam_with_pose/', views.webcam_with_pose, name='webcam_with_pose'),
    path('pose_estimation/', views.pose_estimation, name='pose_estimation'),
    
]
