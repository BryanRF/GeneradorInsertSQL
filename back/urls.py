from django.urls import path
from . import views

urlpatterns = [
    path('generate-data/', views.GenerateDataView.as_view(), name='generate-data'),
    path('export-file/', views.ExportFileView.as_view(), name='export-file'),
    path('generate-code/', views.GenerateCodeView.as_view(), name='generate-code'),
]
