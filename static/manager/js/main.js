
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
