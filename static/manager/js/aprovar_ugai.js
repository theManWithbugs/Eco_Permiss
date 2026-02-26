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

function aprovarUgai() {
  Swal.fire({
    title: "Tem certeza?",
    text: "Você tem certeza que deseja aprovar o uso da UGAI?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    cancelButtonText: "Cancelar",
    confirmButtonText: "Sim, tenho certeza"
  }).then((result) => {
    if (result.isConfirmed) {
      fetch(`/manager/api_aprovar_ugai/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'id': current_id})
      })
      .then(response => response.json())
      .then(data => {
        if (data['status'] == 'ok') {
          window.location.reload();
        } else if(data['status'] == 'error(400)') {
          Swal.fire({
            icon: "error",
            title: "error(400)",
            text: `${data['message']}`,
          });
        }
      });
    }
  });
}