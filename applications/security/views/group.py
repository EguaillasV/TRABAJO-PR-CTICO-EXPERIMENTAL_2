
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.db.models import ProtectedError
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        labels = {'name': 'Nombre del Grupo'}
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 dark:bg-principal dark:text-white',
                'placeholder': 'Ingrese el nombre del grupo'
            })
        }

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'security/group/group_list.html'
    context_object_name = 'groups'

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'security/group/group_form.html'
    success_url = reverse_lazy('security:group_list')

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'security/group/group_form.html'
    success_url = reverse_lazy('security:group_list')

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'security/group/group_delete.html'
    success_url = reverse_lazy('security:group_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return redirect(self.success_url)
        except ProtectedError:
            return render(request, self.template_name, {
                'object': self.object,
                'protected_error': True
            })
