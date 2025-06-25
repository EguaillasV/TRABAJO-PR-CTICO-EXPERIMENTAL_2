from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import Group, Permission
from applications.security.models import GroupModulePermission, Module

@login_required
def permissions_interactive_view(request):
    return render(request, 'security/permissions_interactive.html')

def api_get_modules_by_group(request, group_id):
    permisos = GroupModulePermission.objects.filter(group_id=group_id).select_related('module')
    data = [{'module_id': p.module.id, 'module_name': p.module.name} for p in permisos]
    return JsonResponse(data, safe=False)

def api_get_permissions_by_group_module(request, group_id, module_id):
    relation, _ = GroupModulePermission.objects.get_or_create(group_id=group_id, module_id=module_id)
    all_permissions = Permission.objects.all()
    assigned_ids = relation.permissions.values_list('id', flat=True)

    data = []
    for perm in all_permissions:
        data.append({
            'id': perm.id,
            'name': perm.name,
            'assigned': perm.id in assigned_ids
        })

    return JsonResponse(data, safe=False)
@login_required
def permissions_interactive_embed(request):
    return render(request, 'security/permissions_interactive_embed.html')


def get_modules_by_group(request, group_id):
    # Extrae los módulos asignados al grupo
    modules = GroupModulePermission.objects.filter(group_id=group_id).select_related('module').distinct()

    data = [
        {
            'module_id': perm.module.id,
            'module_name': perm.module.name
        } for perm in modules
    ]

    return JsonResponse(data, safe=False)

def get_user_permissions(self):
    return self.request.user.get_all_permissions()