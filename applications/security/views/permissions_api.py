# applications/security/views/permissions_api.py

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import Group, Permission
from django.shortcuts import get_object_or_404
from applications.security.models import Module, GroupModulePermission
import json

def api_groups(request):
    """GET /auth/api/groups/ → lista de grupos"""
    groups = Group.objects.all().values('id', 'name')
    return JsonResponse({'groups': list(groups)})

def api_modules(request, group_id):
    """GET /auth/api/modules/<group_id>/ → módulos asignados al grupo"""
    modules = Module.objects.filter(
        groupmodulepermission__group_id=group_id
    ).distinct()
    data = [{'id': m.id, 'name': m.name} for m in modules]
    return JsonResponse({'modules': data})

def api_permissions(request, group_id, module_id):
    """
    GET /auth/api/permissions/<group_id>/<module_id>/
    → lista de permisos con flag 'assigned'
    """
    all_permissions = Permission.objects.all()
    try:
        gmp = GroupModulePermission.objects.get(
            group_id=group_id,
            module_id=module_id
        )
        assigned = set(gmp.permissions.values_list('id', flat=True))
    except GroupModulePermission.DoesNotExist:
        assigned = set()

    perms = [{
        'id': p.id,
        'name': p.name,
        'codename': p.codename,
        'assigned': (p.id in assigned)
    } for p in all_permissions]

    return JsonResponse({'permissions': perms})

@csrf_exempt
@require_http_methods(["POST"])
def api_save_permissions(request):
    """
    POST /auth/api/save_permissions/
    Recibe JSON { group_id, module_id, permissions: […] } O bien
               { group_id, module_id, permission_ids: […] }
    Actualiza GroupModulePermission y sincroniza Group.permissions
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('JSON inválido')

    group_id  = data.get("group_id")
    module_id = data.get("module_id")

    # Acepta tanto "permission_ids" como "permissions"
    permission_ids = data.get("permission_ids")
    if permission_ids is None:
        permission_ids = data.get("permissions", [])

    if not group_id or not module_id:
        return HttpResponseBadRequest('Faltan parámetros')

    # Crea o actualiza el registro intermedio
    relation, _ = GroupModulePermission.objects.get_or_create(
        group_id=group_id,
        module_id=module_id
    )
    relation.permissions.set(permission_ids)

    # Sincroniza también la M2M nativa que utiliza el Admin
    group = get_object_or_404(Group, pk=group_id)
    all_perm_ids = GroupModulePermission.objects \
        .filter(group=group) \
        .values_list('permissions__id', flat=True)
    group.permissions.set(
        Permission.objects.filter(id__in=all_perm_ids)
    )

    return JsonResponse({'status': 'ok', 'message': 'Permisos guardados'})

def get_modules_by_group(request, group_id):
    """
    GET /auth/api/get_modules_by_group/<group_id>/
    Devuelve módulos disponibles para ese grupo
    """
    modules = GroupModulePermission.objects.filter(
        group_id=group_id
    ).select_related('module').distinct()

    data = [{
        'module_id': perm.module.id,
        'module_name': perm.module.name
    } for perm in modules]

    return JsonResponse(data, safe=False)   