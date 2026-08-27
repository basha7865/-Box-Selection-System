from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/boxes/', views.manage_boxes_api, name='manage_boxes_api'),
    path('api/boxes/<int:box_id>/', views.box_detail_api, name='box_detail_api'),
]