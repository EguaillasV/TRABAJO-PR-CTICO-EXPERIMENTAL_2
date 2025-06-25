from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, View
from django.contrib import messages
from django.urls import reverse_lazy
from applications.security.models import User
from applications.security.forms.user import UserForm 
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from applications.security.forms import UserForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.db.models import ProtectedError



from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

class UserListView(ListView):
    model = User
    template_name = 'user/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q')
        users = User.objects.all()
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
    form_class = UserForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('security:user_list')

    def form_valid(self, form):
        user = form.save(commit=False)

        # Generar un username automáticamente si está vacío
        if not user.username:
            user.username = user.email or f"user_{User.objects.count() + 1}"

        user.save()
        messages.success(self.request, "✅ Usuario creado correctamente.")
        return redirect(self.success_url)

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm  # Cambiado aquí
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('security:user_list')

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado correctamente.")
        return super().form_valid(form)

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('security:user_list')

    def get(self, *args, **kwargs):
        # No mostramos plantilla de confirmación, solo redirigimos y llamamos delete
        return self.post(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        try:
            messages.success(self.request, "Usuario eliminado correctamente.")
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, "No se puede eliminar este usuario porque tiene datos relacionados.")
            return HttpResponseRedirect(self.success_url)



class UserPasswordChangeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = CustomPasswordChangeForm(user=user)
        return render(request, 'user/user_password_change.html', {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = CustomPasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect('security:user_list')
        return render(request, 'user/user_password_change.html', {'form': form})


def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['permissions'] = self.get_user_permissions()  # ← Asegúrate de esta línea
    return context 