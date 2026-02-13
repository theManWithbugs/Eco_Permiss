const pesquisa = document.getElementById('solic_pesq');
const ugai = document.getElementById('aut_ugai');

const button_pesq = document.getElementById('btn_pesq');
const button_ugai = document.getElementById('btn_ugai');

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

document.addEventListener('DOMContentLoaded', () => {
  mostrar_formulario('solic_pesq');
})