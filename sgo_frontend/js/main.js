document.addEventListener("DOMContentLoaded", () => {
  configurarNavegacion();
  configurarFormularios();
  verificarAPI();
  cargarDashboard();
  cargarPacientes();
  cargarSucursales();
  cargarOdontologos();
  cargarConsultorios();
});

function configurarNavegacion() {
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      document.querySelectorAll(".section").forEach(sec => sec.classList.add("d-none"));
      document.getElementById(btn.dataset.section).classList.remove("d-none");
    });
  });
}

function configurarFormularios() {
  document.getElementById("formLogin").addEventListener("submit", login);
  document.getElementById("formPaciente").addEventListener("submit", guardarPaciente);
  document.getElementById("formSucursal").addEventListener("submit", guardarSucursal);
  document.getElementById("formOdontologo").addEventListener("submit", guardarOdontologo);
  document.getElementById("formConsultorio").addEventListener("submit", guardarConsultorio);
}

function mostrarToast(mensaje) {
  const toast = document.getElementById("toast");
  toast.textContent = mensaje;
  toast.classList.remove("d-none");
  setTimeout(() => toast.classList.add("d-none"), 3000);
}

async function verificarAPI() {
  const apiStatus = document.getElementById("apiStatus");
  try {
    await api.get("/");
    apiStatus.textContent = "API: conectada";
    apiStatus.className = "badge text-bg-success";
  } catch (error) {
    apiStatus.textContent = "API: sin conexión";
    apiStatus.className = "badge text-bg-danger";
  }
}

async function login(event) {
  event.preventDefault();
  try {
    const data = await api.post("/login", {
      usuario: document.getElementById("loginUsuario").value.trim(),
      password: document.getElementById("loginPassword").value.trim(),
    });
    localStorage.setItem("sgo_token", data.token);
    mostrarToast(data.mensaje || "Login correcto");
  } catch (error) {
    mostrarToast(error.message);
  }
}

async function cargarDashboard() {
  try {
    const [pacientes, odontologos, sucursales, consultorios] = await Promise.all([
      api.get("/pacientes"),
      api.get("/odontologos"),
      api.get("/sucursales"),
      api.get("/consultorios"),
    ]);
    document.getElementById("totalPacientes").textContent = pacientes.length;
    document.getElementById("totalOdontologos").textContent = odontologos.length;
    document.getElementById("totalSucursales").textContent = sucursales.length;
    document.getElementById("totalConsultorios").textContent = consultorios.length;
  } catch (error) {
    mostrarToast("No se pudo cargar el dashboard");
  }
}

async function guardarPaciente(event) {
  event.preventDefault();
  const paciente = {
    num_a: Number(document.getElementById("p_num_a").value),
    tipoafiliado: document.getElementById("p_tipoafiliado").value,
    costo_m: Number(document.getElementById("p_costo_m").value),
    id_cedula: Number(document.getElementById("p_id_cedula").value),
    nomp: document.getElementById("p_nomp").value.trim(),
    app: document.getElementById("p_app").value.trim(),
    amp: document.getElementById("p_amp").value.trim(),
    monto_mensual: Number(document.getElementById("p_monto_mensual").value),
    telefono: Number(document.getElementById("p_telefono").value),
  };
  try {
    const data = await api.post("/pacientes", paciente);
    mostrarToast(data.mensaje || "Paciente guardado");
    event.target.reset();
    await cargarPacientes();
    await cargarDashboard();
  } catch (error) {
    mostrarToast(error.message);
  }
}

async function cargarPacientes() {
  const tbody = document.getElementById("tablaPacientes");
  try {
    const pacientes = await api.get("/pacientes");
    tbody.innerHTML = pacientes.length ? pacientes.map(p => `
      <tr>
        <td>${p.id_cedula}</td>
        <td>${p.nomp} ${p.app} ${p.amp || ""}</td>
        <td>$${p.monto_mensual}</td>
        <td>${p.num_a}</td>
        <td><button class="btn btn-danger btn-sm" onclick="eliminarPaciente(${p.id_cedula})">Eliminar</button></td>
      </tr>`).join("") : `<tr><td colspan="5" class="text-center">No hay pacientes.</td></tr>`;
  } catch (error) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-danger text-center">No se pudieron cargar pacientes.</td></tr>`;
  }
}

async function eliminarPaciente(id) {
  if (!confirm("¿Eliminar paciente?")) return;
  try {
    const data = await api.delete(`/pacientes/${id}`);
    mostrarToast(data.mensaje || "Paciente eliminado");
    await cargarPacientes();
    await cargarDashboard();
  } catch (error) {
    mostrarToast(error.message);
  }
}

async function guardarSucursal(event) {
  event.preventDefault();
  const sucursal = {
    id_sucursal: Number(document.getElementById("s_id_sucursal").value),
    nombre_s: document.getElementById("s_nombre_s").value.trim(),
    calle: document.getElementById("s_calle").value.trim(),
    numero: Number(document.getElementById("s_numero").value),
    ciudad: document.getElementById("s_ciudad").value.trim(),
  };
  try {
    const data = await api.post("/sucursales", sucursal);
    mostrarToast(data.mensaje || "Sucursal guardada");
    event.target.reset();
    await cargarSucursales();
    await cargarDashboard();
  } catch (error) {
    mostrarToast(error.message);
  }
}

async function cargarSucursales() {
  const tbody = document.getElementById("tablaSucursales");
  try {
    const sucursales = await api.get("/sucursales");
    tbody.innerHTML = sucursales.length ? sucursales.map(s => `
      <tr>
        <td>${s.id_sucursal}</td>
        <td>${s.nombre_s}</td>
        <td>${s.calle} #${s.numero}</td>
        <td>${s.ciudad}</td>
        <td><button class="btn btn-danger btn-sm" onclick="eliminarSucursal(${s.id_sucursal})">Eliminar</button></td>
      </tr>`).join("") : `<tr><td colspan="5" class="text-center">No hay sucursales.</td></tr>`;
  } catch (error) {
    tbody.innerHTML = `<tr><td colspan="5" class="text-danger text-center">No se pudieron cargar sucursales.</td></tr>`;
  }
}

async function eliminarSucursal(id) {
  if (!confirm("¿Eliminar sucursal?")) return;
  try {
    const data = await api.delete(`/sucursales/${id}`);
    mostrarToast(data.mensaje || "Sucursal eliminada");
    await cargarSucursales();
    await cargarDashboard();
  } catch (error) {
    mostrarToast(error.message);
  }
}

function convertirFechaLocalAApi(valor) {
  return valor ? valor.replace("T", " ") : "";
}

async function guardarOdontologo(event) {
  event.preventDefault();
  const odontologo = {
    cedula: Number(document.getElementById("o_cedula").value),
    horario_con: convertirFechaLocalAApi(document.getElementById("o_horario_con").value),
    horario_suc: convertirFechaLocalAApi(document.getElementById("o_horario_suc").value),
    especialidad: document.getElementById("o_especialidad").value.trim(),
    nomo: document.getElementById("o_nomo").value.trim(),
    apo: document.getElementById("o_apo").value.trim(),
    amo: document.getElementById("o_amo").value.trim(),
    num_cos: Number(document.getElementById("o_num_cos").value),
    id_sucursal: Number(document.getElementById("o_id_sucursal").value),
  };
  try {
    const data = await api.post("/odontologos", odontologo);
    mostrarToast(data.mensaje || "Odontólogo guardado");
    event.target.reset();
    await cargarOdontologos();
    await cargarDashboard();
  } catch (error) {
    mostrarToast(error.message);
  }
}

async function cargarOdontologos() {
  const tbody = document.getElementById("tablaOdontologos");
  try {
    const odontologos = await api.get("/odontologos");
    tbody.innerHTML = odontologos.length ? odontologos.map(o => `
      <tr>
        <td>${o.cedula}</td>
        <td>${o.nomo} ${o.apo} ${o.amo || ""}</td>
        <td>${o.especialidad}</td>
        <td>${o.num_cos}</td>
        <td>${o.id_sucursal}</td>
        <td><button class="btn btn-danger btn-sm" onclick="eliminarOdontologo(${o.cedula})">Eliminar</button></td>
      </tr>`).join("") : `<tr><td colspan="6" class="text-center">No hay odontólogos.</td></tr>`;
  } catch (error) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-danger text-center">No se pudieron cargar odontólogos.</td></tr>`;
  }
}

async function eliminarOdontologo(cedula) {
  if (!confirm("¿Eliminar odontólogo?")) return;
  try {
    const data = await api.delete(`/odontologos/${cedula}`);
    mostrarToast(data.mensaje || "Odontólogo eliminado");
    await cargarOdontologos();
    await cargarDashboard();
  } catch (error) {
    mostrarToast(error.message);
  }
}

async function guardarConsultorio(event) {
  event.preventDefault();
  const consultorio = {
    num_cos: Number(document.getElementById("c_num_cos").value),
    id_sucursal: Number(document.getElementById("c_id_sucursal").value),
  };
  try {
    const data = await api.post("/consultorios", consultorio);
    mostrarToast(data.mensaje || "Consultorio guardado");
    event.target.reset();
    await cargarConsultorios();
    await cargarDashboard();
  } catch (error) {
    mostrarToast(error.message);
  }
}

async function cargarConsultorios() {
  const tbody = document.getElementById("tablaConsultorios");
  try {
    const consultorios = await api.get("/consultorios");
    tbody.innerHTML = consultorios.length ? consultorios.map(c => `
      <tr>
        <td>${c.num_cos}</td>
        <td>${c.id_sucursal}</td>
        <td><button class="btn btn-danger btn-sm" onclick="eliminarConsultorio(${c.id_sucursal}, ${c.num_cos})">Eliminar</button></td>
      </tr>`).join("") : `<tr><td colspan="3" class="text-center">No hay consultorios.</td></tr>`;
  } catch (error) {
    tbody.innerHTML = `<tr><td colspan="3" class="text-danger text-center">No se pudieron cargar consultorios.</td></tr>`;
  }
}

async function eliminarConsultorio(idSucursal, numCos) {
  if (!confirm("¿Eliminar consultorio?")) return;
  try {
    const data = await api.delete(`/consultorios/${idSucursal}/${numCos}`);
    mostrarToast(data.mensaje || "Consultorio eliminado");
    await cargarConsultorios();
    await cargarDashboard();
  } catch (error) {
    mostrarToast(error.message);
  }
}
