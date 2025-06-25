from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, Permission
from applications.security.models import Module, GroupModulePermission
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

def group_permission_view(request):
    groups = Group.objects.all().order_by('name')
    return render(request, 'security/group_permissions.html', {'groups': groups})


def get_group_modules(request, group_id):
    modules = Module.objects.filter(is_active=True).order_by('menu__order', 'order')
    assigned = GroupModulePermission.objects.filter(group_id=group_id).select_related('module')

    assigned_dict = {
        str(item.module.id): list(item.permissions.values_list('codename', flat=True))
        for item in assigned
    }

    # Obtener permisos específicos por módulo
    permissions_by_module = {}
    for module in modules:
        perms = module.permissions.all().values('id', 'name', 'codename')
        permissions_by_module[str(module.id)] = list(perms)

    return JsonResponse({
        'modules': list(modules.values('id', 'name', 'url', 'menu__name')),
        'assigned': assigned_dict,
        'permissions_by_module': permissions_by_module,
    })



@csrf_exempt
def save_group_permissions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_id = data.get('group_id')
        permissions_by_module = data.get('permissions')  # {module_id: [codename, ...]}

        if not group_id:
            return HttpResponseBadRequest("Grupo no especificado")

        group = get_object_or_404(Group, pk=group_id)

        # Eliminar previas configuraciones
        GroupModulePermission.objects.filter(group=group).delete()

        for module_id, perm_codenames in permissions_by_module.items():
            module = get_object_or_404(Module, pk=module_id)
            gmp = GroupModulePermission.objects.create(group=group, module=module)
            perms = Permission.objects.filter(codename__in=perm_codenames)
            gmp.permissions.set(perms)

        return JsonResponse({'status': 'success'})

    return HttpResponseBadRequest("Método no permitido")
