// Cambia esta URL solo si Flask corre en otro puerto o dominio.
const API_URL = "http://localhost:5000";

async function requestAPI(endpoint, options = {}) {
  const response = await fetch(`${API_URL}${endpoint}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  let data = null;
  try {
    data = await response.json();
  } catch (_) {
    data = {};
  }

  if (!response.ok) {
    throw new Error(data.error || data.detalle || "Error al comunicarse con la API");
  }

  return data;
}

const api = {
  get: (endpoint) => requestAPI(endpoint),
  post: (endpoint, body) => requestAPI(endpoint, { method: "POST", body: JSON.stringify(body) }),
  put: (endpoint, body) => requestAPI(endpoint, { method: "PUT", body: JSON.stringify(body) }),
  delete: (endpoint) => requestAPI(endpoint, { method: "DELETE" }),
};
