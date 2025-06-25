from django.urls import path
from . import views

app_name = "pacientes"

urlpatterns = [
    path('', views.PatientListView.as_view(), name='list'),
    path('crear/', views.PatientCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.PatientUpdateView.as_view(), name='update'),
    path('<int:pk>/eliminar/', views.PatientDeleteView.as_view(), name='delete'),
]
