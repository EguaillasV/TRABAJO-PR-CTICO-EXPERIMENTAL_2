from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Diagnosis

class DiagnosisListView(ListView):
    model = Diagnosis
    template_name = 'diagnosticos/list.html'
    context_object_name = 'diagnosticos'

class DiagnosisCreateView(CreateView):
    model = Diagnosis
    fields = ['patient', 'description', 'icd_code', 'notes', 'is_active']
    template_name = 'diagnosticos/form.html'
    success_url = reverse_lazy('diagnosticos:list')

class DiagnosisUpdateView(UpdateView):
    model = Diagnosis
    fields = ['patient', 'description', 'icd_code', 'notes', 'is_active']
    template_name = 'diagnosticos/form.html'
    success_url = reverse_lazy('diagnosticos:list')

class DiagnosisDeleteView(DeleteView):
    model = Diagnosis
    template_name = 'diagnosticos/confirm_delete.html'
    success_url = reverse_lazy('diagnosticos:list')

class MenuDiagnosticoView(TemplateView):
    template_name = "diagnosticos/form.html"
