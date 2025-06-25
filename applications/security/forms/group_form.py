from django import forms
from django.contrib.auth.models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nombre del grupo',
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:bg-principal dark:text-gray-300'
            }),
        }
        labels = {
            'name': 'Nombre del grupo',
        }
