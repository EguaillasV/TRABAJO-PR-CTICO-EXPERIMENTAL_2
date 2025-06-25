from django.urls import path
from .views import (
    DiagnosisCreateView,
    DiagnosisListView,
    DiagnosisUpdateView,
    DiagnosisDeleteView
)
from applications.security.views.home import ModuloTemplateView

app_name = "diagnosticos"

urlpatterns = [
    path('crear/', DiagnosisCreateView.as_view(), name='create'),
    path('lista/', DiagnosisListView.as_view(), name='list'),
    path('editar/<int:pk>/', DiagnosisUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>/', DiagnosisDeleteView.as_view(), name='delete'),
    path('modulos/', ModuloTemplateView.as_view(), name='module_list'),
]
