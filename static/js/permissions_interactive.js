const groupSelect         = document.getElementById("group-select");
const moduleSelect        = document.getElementById("module-select");
const permissionsContainer = document.getElementById("permissions-container");
const permissionsForm     = document.getElementById("permissions-form");
const saveButton          = document.getElementById("save-permissions");

document.addEventListener("DOMContentLoaded", () => {
  // 1) Cargar grupos
  fetch("/auth/api/groups/")
    .then(res => res.json())
    .then(groups => {
      groups.forEach(g => {
        const opt = document.createElement("option");
        opt.value = g.id;
        opt.textContent = g.name;
        groupSelect.appendChild(opt);
      });
    });

  // 2) Cambiar grupo → recargar módulos
  groupSelect.addEventListener("change", () => {
    const gid = groupSelect.value;
    moduleSelect.innerHTML = '<option value="">-- Seleccione --</option>';
    permissionsForm.innerHTML = "";
    permissionsContainer.classList.add("hidden");
    if (!gid) return;

    fetch(`/auth/api/modules/${gid}/`)
      .then(res => res.json())
      .then(mods => {
        mods.forEach(m => {
          const opt = document.createElement("option");
          opt.value = m.module_id;
          opt.textContent = m.module_name;
          moduleSelect.appendChild(opt);
        });
      });
  });

  // 3) Cambiar módulo → recargar permisos (todos) y marcar los asignados
  moduleSelect.addEventListener("change", () => {
    const gid = groupSelect.value;
    const mid = moduleSelect.value;
    permissionsForm.innerHTML = "";
    permissionsContainer.classList.add("hidden");
    if (!gid || !mid) return;

    fetch(`/auth/api/permissions/${gid}/${mid}/`)
      .then(res => res.json())
      .then(perms => {
        if (!perms.length) {
          permissionsForm.innerHTML = "<p class='text-sm text-gray-500'>No hay permisos en este módulo.</p>";
        } else {
          perms.forEach(p => {
            const row = document.createElement("div");
            row.className = "flex items-center space-x-2";

            const cb = document.createElement("input");
            cb.type    = "checkbox";
            cb.value   = p.id;
            cb.checked = p.assigned;            // ← marcamos los asignados
            cb.classList.add("mr-2");

            const lbl = document.createElement("label");
            lbl.textContent = p.name;

            row.append(cb, lbl);
            permissionsForm.append(row);
          });
        }
        permissionsContainer.classList.remove("hidden");
      });
  });

  // 4) Guardar permisos
  saveButton.addEventListener("click", () => {
    const gid = groupSelect.value;
    const mid = moduleSelect.value;
    if (!gid || !mid) return;

    const selected = Array.from(
      permissionsForm.querySelectorAll("input[type='checkbox']")
    )
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
        group_id: gid,
        module_id: mid,
        permission_ids: selected
      }),
    })
    .then(r => r.json())
    .then(js => {
      alert(js.message || "Permisos guardados correctamente.");
      limpiarFormulario();
    });
  });
});

function limpiarFormulario() {
  groupSelect.selectedIndex = 0;
  moduleSelect.innerHTML    = '<option value="">-- Seleccione --</option>';
  permissionsForm.innerHTML = "";
  permissionsContainer.classList.add("hidden");
}

function getCSRFToken() {
  const name = "csrftoken";
  return document.cookie.split(";")
    .map(c => c.trim().split("="))
    .find(([k]) => k === name)?.[1] || "";
}
