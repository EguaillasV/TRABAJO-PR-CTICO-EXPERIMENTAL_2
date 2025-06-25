const groupSelect = document.getElementById("group-select");
const moduleSelect = document.getElementById("module-select");
const permissionsContainer = document.getElementById("permissions-container");
const permissionsForm = document.getElementById("permissions-form");
const saveButton = document.getElementById("save-permissions");

// Cargar grupos
fetch("/auth/api/groups/")
  .then(res => res.json())
  .then(data => {
    data.forEach(group => {
      const option = document.createElement("option");
      option.value = group.id;
      option.textContent = group.name;
      groupSelect.appendChild(option);
    });
  });

// Al seleccionar grupo, cargar módulos
groupSelect.addEventListener("change", () => {
  const groupId = groupSelect.value;
  moduleSelect.innerHTML = '<option value="">-- Seleccione --</option>';
  permissionsContainer.classList.add("hidden");

  if (!groupId) return;

  fetch(`/auth/api/modules/${groupId}/`)
    .then(res => res.json())
    .then(modules => {
      modules.forEach(mod => {
        const option = document.createElement("option");
        option.value = mod.module_id;
        option.textContent = mod.module_name;
        moduleSelect.appendChild(option);
      });
    });
});

// Al seleccionar módulo, cargar permisos
moduleSelect.addEventListener("change", () => {
  const groupId = groupSelect.value;
  const moduleId = moduleSelect.value;
  permissionsForm.innerHTML = "";
  permissionsContainer.classList.add("hidden");

  if (!groupId || !moduleId) return;

  fetch(`/auth/api/permissions/${groupId}/${moduleId}/`)
    .then(res => res.json())
    .then(perms => {
      perms.forEach(perm => {
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.name = "permissions";
        checkbox.value = perm.id;
        checkbox.checked = perm.assigned;
        checkbox.classList.add("mr-2");

        const label = document.createElement("label");
        label.classList.add("flex", "items-center", "space-x-2");
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(perm.name));

        permissionsForm.appendChild(label);
      });

      permissionsContainer.classList.remove("hidden");
    });
});

// Función pura JS para limpiar el formulario
function limpiarFormulario() {
  // Reiniciar selects y ocultar permisos
  groupSelect.selectedIndex = 0;
  moduleSelect.innerHTML = '<option value="">-- Seleccione --</option>';
  permissionsForm.innerHTML = '';
  permissionsContainer.classList.add('hidden');
}

// Guardar permisos
saveButton.addEventListener("click", () => {
  const groupId = groupSelect.value;
  const moduleId = moduleSelect.value;
  const checked = [...permissionsForm.querySelectorAll("input[type='checkbox']")]
    .filter(cb => cb.checked)
    .map(cb => cb.value);

  fetch("/auth/api/save_permissions/", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCSRFToken(),
    },
    body: JSON.stringify({
      group_id: groupId,
      module_id: moduleId,
      permissions: checked,
    }),
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || "Permisos guardados correctamente.");
      // Reinicia el formulario con JS puro
      limpiarFormulario();
    });
});

function getCSRFToken() {
  const name = "csrftoken";
  const cookies = document.cookie.split(";");
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split("=");
    if (key === name) return decodeURIComponent(value);
  }
}
