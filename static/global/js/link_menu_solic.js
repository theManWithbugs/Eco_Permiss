const pesquisa = document.getElementById('solic_pesq');
const ugai = document.getElementById('aut_ugai');

const button_pesq = document.getElementById('btn_pesq');
const button_ugai = document.getElementById('btn_ugai');

const form_pesq = document.getElementById('form_pesquisa');

function mostrar_formulario(value) {
  pesquisa.style.display = 'none';
  ugai.style.display = 'none';

  if (value === 'solic_pesq') {
    pesquisa.style.display = 'block';
  }else if ( value === 'aut_ugai' ) {
    ugai.style.display = 'block';
  }
}

function current_button(value) {
  if (value === 1) {

  } else if (value === 2){

  }
}

function aceite_termos_PESQ() {
  Swal.fire({
    title: "Confirmar aceite",
    text: "Você confirma que fez a leitura e aceita os termos de commpromisso, assunção de risco e boas praticas?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Sim, enviar",
    cancelButtonText: "Cancelar",
    background: "#FFFFFF"
  }).then((result) => {
    if (!result.isConfirmed) {
      return;
    } else {
      form_pesq.submit()
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  mostrar_formulario('solic_pesq');
})