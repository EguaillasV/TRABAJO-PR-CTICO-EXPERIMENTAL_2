from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import Group
from applications.security.models import GroupModulePermission, Module

@login_required
def permissions_interactive_view(request):
    return render(request, 'security/permissions_interactive.html')


def api_get_modules_by_group(request, group_id):
    permisos = GroupModulePermission.objects.filter(
        group_id=group_id
    ).select_related('module')
    data = [
        {'module_id': p.module.id, 'module_name': p.module.name}
        for p in permisos
    ]
    return JsonResponse(data, safe=False)


def api_get_permissions_by_group_module(request, group_id, module_id):
    """
    GET /auth/api/permissions/<group_id>/<module_id>/
    → devuelve solo los permisos que ese grupo tiene asignados para el módulo
    """
    try:
        relation = GroupModulePermission.objects.get(
            group_id=group_id,
            module_id=module_id
        )
        assigned_perms = relation.permissions.all()
    except GroupModulePermission.DoesNotExist:
        assigned_perms = []

    data = [
        {'id': p.id, 'name': p.name, 'codename': p.codename}
        for p in assigned_perms
    ]
    return JsonResponse(data, safe=False)

@login_required
def permissions_interactive_embed(request):
    return render(request, 'security/permissions_interactive_embed.html')


def get_modules_by_group(request, group_id):
    modules = GroupModulePermission.objects.filter(
        group_id=group_id
    ).select_related('module').distinct()
    data = [
        {'module_id': perm.module.id, 'module_name': perm.module.name}
        for perm in modules
    ]
    return JsonResponse(data, safe=False)


def get_user_permissions(self):
    return self.request.user.get_all_permissions()
