from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Patient

class PatientListView(ListView):
    model = Patient
    template_name = 'pacientes/list.html'
    context_object_name = 'pacientes'


class PatientCreateView(CreateView):
    model = Patient
    template_name = 'pacientes/form.html'
    fields = '__all__'
    success_url = reverse_lazy('pacientes:list')


class PatientUpdateView(UpdateView):
    model = Patient
    template_name = 'pacientes/form.html'
    fields = '__all__'
    success_url = reverse_lazy('pacientes:list')


class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'pacientes/confirm_delete.html'
    success_url = reverse_lazy('pacientes:list')
