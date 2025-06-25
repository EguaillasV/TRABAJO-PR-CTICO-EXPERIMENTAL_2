from django.urls import path
from django.http import JsonResponse
from django.contrib.auth.models import Group

from applications.security.views.auth import signin, signout
from applications.security.views.menu import MenuCreateView, MenuDeleteView, MenuListView, MenuUpdateView
from applications.security.views.module import ModuleCreateView, ModuleDeleteView, ModuleListView, ModuleUpdateView
from applications.security.views.menu_diagnostico import MenuDiagnosticoView
from applications.security.views.group_permission import group_permission_view, get_group_modules, save_group_permissions
from applications.security.views.permissions_api import api_groups, api_modules, api_permissions, api_save_permissions
from applications.security.views.permissions_ui import permissions_interactive_view, api_get_modules_by_group, api_get_permissions_by_group_module,permissions_interactive_embed
from applications.security.views.group import GroupListView, GroupCreateView, GroupUpdateView, GroupDeleteView
from applications.security.views.user import UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserPasswordChangeView



app_name = 'security'

urlpatterns = [
    # rutas de módulos
    path('module_list/', ModuleListView.as_view(), name="module_list"),
    path('module_create/', ModuleCreateView.as_view(), name="module_create"),
    path('module_update/<int:pk>/', ModuleUpdateView.as_view(), name='module_update'),
    path('module_delete/<int:pk>/', ModuleDeleteView.as_view(), name='module_delete'),

    # rutas de menús
    path('menu_list/', MenuListView.as_view(), name="menu_list"),
    path('menu_create/', MenuCreateView.as_view(), name="menu_create"),
    path('menu_update/<int:pk>/', MenuUpdateView.as_view(), name='menu_update'),
    path('menu_delete/<int:pk>/', MenuDeleteView.as_view(), name='menu_delete'),
    
    # rutas de grupos
    path('group_list/', GroupListView.as_view(), name='group_list'),
    path('group_create/', GroupCreateView.as_view(), name='group_create'),
    path('group_update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
    path('group_delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),

    # rutas de usuarios
    path('usuarios/', UserListView.as_view(), name='user_list'),
    path('usuarios/crear/', UserCreateView.as_view(), name='user_create'),
    path('usuarios/<int:pk>/editar/', UserUpdateView.as_view(), name='user_update'),
    path('usuarios/<int:pk>/eliminar/', UserDeleteView.as_view(), name='user_delete'),
    path('usuarios/<int:pk>/password/', UserPasswordChangeView.as_view(), name='user_password_change'),

    # rutas de autenticación
    path('logout/', signout, name='signout'),
    path('signin/', signin, name='signin'),

    # otros menús
    path('menu_diagnostico/', MenuDiagnosticoView.as_view(), name='menu_diagnostico'),

    # rutas de permisos tradicionales
    path('group-permissions/', group_permission_view, name='group_permissions'),
    path('group-modules/<int:group_id>/', get_group_modules, name='get_group_modules'),
    path('save-group-permissions/', save_group_permissions, name='save_group_permissions'),

    # rutas para el módulo interactivo
    path('api/groups/', lambda request: JsonResponse(list(Group.objects.values('id', 'name')), safe=False)),
    path('api/modules/<int:group_id>/', api_get_modules_by_group),
    path('api/permissions/<int:group_id>/<int:module_id>/', api_get_permissions_by_group_module),
    path('api/save_permissions/', api_save_permissions),

    # Vista interactiva HTML
    path('permissions_interactive/', permissions_interactive_view, name='permissions_interactive'),
    path('permissions_embed/', permissions_interactive_embed, name='permissions_embed'),

]
