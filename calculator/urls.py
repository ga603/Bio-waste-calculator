from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculator_view, name='calculator'),
    path('download-report/<int:result_id>/', views.download_pdf_report, name='download_pdf'),
]