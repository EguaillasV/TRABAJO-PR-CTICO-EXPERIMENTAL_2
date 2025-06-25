
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group, Permission, User
from django.shortcuts import render

from applications.security.models import Module, GroupModulePermission
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import json

class MenuDiagnosticoView(TemplateView):
    template_name = "security/menu_diagnostico.html"

def api_groups(request):
    grupos = Group.objects.all().values('id', 'name')
    return JsonResponse(list(grupos), safe=False)

def api_modules(request, group_id):
    permisos = GroupModulePermission.objects.filter(group_id=group_id).select_related('module')
    data = [{'module_id': p.module.id, 'module_name': p.module.name} for p in permisos]
    return JsonResponse(data, safe=False)

def api_permissions(request, group_id, module_id):
    group = Group.objects.get(id=group_id)
    permisos_asignados = GroupModulePermission.objects.filter(group=group, module_id=module_id).values_list('permissions__id', flat=True)
    all_permissions = Permission.objects.all()

    data = []
    for perm in all_permissions:
        data.append({
            'id': perm.id,
            'name': perm.name,
            'assigned': perm.id in permisos_asignados
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def api_save_permissions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_id = data.get('group_id')
        module_id = data.get('module_id')
        permisos_ids = data.get('permissions', [])

        relation, _ = GroupModulePermission.objects.get_or_create(
            group_id=group_id,
            module_id=module_id
        )
        relation.permissions.set(permisos_ids)
        return JsonResponse({'message': 'Permisos guardados correctamente.'})

    def permissions_interactive_embed(request):
        return render(request, 'security/permissions_interactive_embed.html') 
    

class UserListView(ListView):
    model = User
    template_name = 'user/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q')
        users = User.objects.all().order_by('id')  # 👈 Ordena por ID como número

        if query:
            users = users.filter(
            email__icontains=query
        ) | users.filter(
            first_name__icontains=query
        ) | users.filter(
            last_name__icontains=query
        )
        return users

class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, "Usuario creado correctamente.")
        return super().form_valid(form)

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('security:user_list')

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado correctamente.")
        return super().form_valid(form)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'user/user_confirm_delete.html'
    success_url = reverse_lazy('security:user_list')   

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Usuario eliminado correctamente.")
        return super().delete(request, *args, **kwargs)

class UserPasswordChangeView(FormView):
    template_name = 'user/user_password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('user_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "Contraseña actualizada correctamente.")
        return super().form_valid(form)
