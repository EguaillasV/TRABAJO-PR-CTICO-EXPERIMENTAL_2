
from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.security.forms.menu import MenuForm
from applications.security.forms.module import ModuleForm
from applications.security.models import Menu, Module
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q


class MenuListView(ListView):
    model = Menu
    template_name = 'security/menus/list.html'
    context_object_name = 'menus'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["permissions"] = {
            "add_menu": user.has_perm("security.add_menu"),
            "change_menu": user.has_perm("security.change_menu"),
            "delete_menu": user.has_perm("security.delete_menu"),
        }
        context["title"] = "Gestión de Menús"
        context["title1"] = "Listado de Menús"
        return context



class MenuCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Menu
    template_name = 'security/menus/form.html'
    form_class = MenuForm
    success_url = reverse_lazy('security:menu_list')
    permission_required = 'add_menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Menu'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        menu = self.object
        messages.success(self.request, f"Éxito al crear el menu {menu.name}.")
        return response


class MenuUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Menu
    template_name = 'security/menus/form.html'
    form_class = MenuForm
    success_url = reverse_lazy('security:menu_list')
    permission_required = 'change_menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Menu'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        menu = self.object
        messages.success(self.request, f"Éxito al actualizar el menu {menu.name}.")
        return response


class MenuDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Menu
    template_name = 'core/delete.html'
    success_url = reverse_lazy('security:menu_list')
    permission_required = 'delete_menu'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Menu'
        context['description'] = f"¿Desea eliminar el menu: {self.object.name}?"
        context['back_url'] = self.success_url
        return context

    
    def form_valid(self, form):
        # Guardar info antes de eliminar
        menu_name = self.object.name
        
        # Llamar al delete del padre
        response = super().form_valid(form)
        
        # Agregar mensaje
        messages.success(self.request, f"Éxito al eliminar lógicamente el menu {menu_name}.")
        
        return response