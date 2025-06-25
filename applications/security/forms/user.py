# applications/security/forms/user.py

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
from applications.security.models import User

class UserForm(forms.ModelForm):
    # 1) Definimos el campo de grupos
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control text-black',
            'size': '6',
        }),
        label="Grupos"
    )

    class Meta:
        model = User
        # 2) Incluimos 'groups' en los campos
        fields = [
            'first_name', 'last_name', 'email', 'dni',
            'phone', 'direction', 'image', 'groups'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control text-black'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control text-black'}),
            'email'     : forms.EmailInput(attrs={'class': 'form-control text-black'}),
            'dni'       : forms.TextInput(attrs={'class': 'form-control text-black'}),
            'phone'     : forms.TextInput(attrs={'class': 'form-control text-black'}),
            'direction' : forms.TextInput(attrs={'class': 'form-control text-black'}),
            'image'     : forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("⚠️ Ya existe un usuario con este correo.")
        return email

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        qs = User.objects.filter(dni=dni)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("⚠️ Ya existe un usuario con este número de DNI.")
        return dni

    def save(self, commit=True):
        # 3) Guardamos primero el usuario
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
            # 4) Luego guardamos la relación M2M
            self.save_m2m()
        return user


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 bg-gray-100 text-black focus:outline-none focus:ring-2 focus:ring-indigo-500'
            })
