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

function resp_message(status, message) {
  let config = {};

  if ([400, 401, 403, 404].includes(status)) {
    config = {
      icon: "error",
      title: "Erro",
      text: message,
      showConfirmButton: false,
      timer: 1500,
      position: 'top'
    };
  } else if ([405, 409, 422, 500, 503].includes(status)) {
    config = {
      icon: "warning",
      title: "Alerta",
      text: message,
      showConfirmButton: false,
      timer: 1500,
      position: 'top'
    };
  } else {
    config = {
      icon: "success",
      title: "Sucesso",
      text: message,
      showConfirmButton: false,
      timer: 1500,
      position: 'top'
    };
  }

  //Aqui abre os sweet alert com essas configurações
  Swal.fire(config).then(() => {
    window.location.reload();
  });
}

async function aprovarPesq() {

  const result = await Swal.fire({
    title: "Tem certeza?",
    text: "Você tem certeza que deseja aprovar a pesquisa?",
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
    const response = await fetch(`/manager/api_aprovar_pesq/`, {
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
