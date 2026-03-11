// ✅ Sucesso
// 200 — OK
// 201 — Created
// 204 — No Content

// ⚠️ Erro do cliente
// 400 — Bad Request
// 401 — Unauthorized
// 405 Method Not Allowed
// 403 — Forbidden
// 404 — Not Found
// 409 — Conflict
// 422 — Unprocessable Entity

// 💥 Erro do servidor
// 500 — Internal Server Error
// 503 — Service Unavailable

//O método includes verifica se o valor passado existe dentro do array
const pathParts = window.location.pathname.split('/');
const current_id = pathParts[3];

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

async function aprovarUgai() {
  const result = await Swal.fire({
    title: "Tem certeza?",
    text: "Você tem certeza que deseja aprovar o uso da UGAI?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    cancelButtonText: "Cancelar",
    confirmButtonText: "Sim, tenho certeza",
    position: 'top'
  });

  if (!result.isConfirmed) {
    return;
  }

  try {
    const response = await fetch(`/manager/api_aprovar_ugai/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({ id: current_id })
    });

    let data = {};

    if (response.status !== 204) {
      data = await response.json();
    }

    resp_message(response.status, data.message || "Operação realizada.");

  } catch (error) {
    resp_message(500, "Erro de conexão com o servidor.");
  }
}

async function recusarUsoUgai() {
  const { value: text } = await Swal.fire({
    input: "textarea",
    inputLabel: "Motivo",
    inputPlaceholder: "Digite aqui...",
    inputAttributes: {
      "aria-label": "Type your message here"
    },
    showCancelButton: true,
    position: 'top'
  });
  if (text) {
    try {
      const response =  await fetch(`/manager/api_recusar_uso_ugai/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ id: current_id, motivo: text })
      });

      let data = {}

      resp_message(response.status, data.message || "Operação realizada.");
    } catch (error) {
      resp_message(500, "Erro de conexão com o servidor.");
    }
  }
}