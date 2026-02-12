let currentStatus;
let paginaAtual = 1;

const div_items = document.getElementById('div_items');

function render_items(items) {
  div_items.innerHTML = '';
  div_items.style = 'margin-top:20px';

  items.forEach(item => {
    const card = document.createElement('div');
    card.className = 'card_items';

    const titulo = document.createElement('h5');
    titulo.textContent = item.acao_realizada;

    const partesData = item.data_solicitacao.split('-');
    const data = document.createElement('p');

    data.textContent =
      `Data da solicitação: ${partesData[2]}/${partesData[1]}/${partesData[0]}`;

    const link = document.createElement('a');
    link.textContent = 'Ver detalhes';
    link.href =
      `#`;

    card.append(titulo, data, link)
    div_items.append(card);
  })
}

function carregarPagina(numeroDaPagina, newStatus) {
  btnAnterior = true;
  btnProximo = true;
  fetch(`/manager/api_resp_pesq/?status=${newStatus}&page=${numeroDaPagina}`, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
    console.log('API Response:', data);
    render_items(data.objs);
    currentStatus = newStatus;
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  carregarPagina(1, false)
})
