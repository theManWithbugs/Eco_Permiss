let currentStatus;
let paginaAtual = 1;

const url_atual = '/manager/info_ugai/';

const div_items = document.getElementById('div_items');
const btnAnterior = document.getElementById('btn-anterior');
const btnProximo = document.getElementById('btn-proximo');
const infoPaginaSpan = document.getElementById('info-pagina');

const pesqInativas = document.getElementById('pesqInativas');
const pesqAtivas = document.getElementById('pesqAtivas');

const div_title = document.getElementById('title_page');
function currentIcon(value) {
  // Limpa o destaque de todos
  const cards = [
    document.getElementById('pesqInativas'),
    document.querySelectorAll('#pesqAtivas')[0],
    document.querySelectorAll('#pesqAtivas')[1],
    document.querySelectorAll('#pesqAtivas')[2]
  ];
  cards.forEach(card => card.style.borderColor = 'silver');

  switch (value) {
    case 1:
      cards[0].style.borderColor = 'black';
      div_title.textContent = '(Solicitações de UGAI | PENDENTES)';
      break;
    case 2:
      cards[1].style.borderColor = 'black';
      div_title.textContent = '(Solicitações de UGAI | APROVADAS)';
      break;
    case 3:
      cards[2].style.borderColor = 'black';
      div_title.textContent = '(Solicitações de UGAI | INVALIDADAS)';
      break;
    case 4:
      cards[3].style.borderColor = 'black';
      div_title.textContent = '(Solicitações de UGAI | ENCERRADAS)';
      break;
  }
}

function render_items(items) {
  div_items.innerHTML = '';
  div_items.style = 'margin-top:20px';

  items.forEach(item => {
    const card = document.createElement('div');
    card.className = 'card_items';

    const titulo = document.createElement('h5');
    titulo.textContent = item.ativ_desenv;

    const partesData = item.data_solicitacao.split('-');
    const data = document.createElement('p');

    data.textContent =
      `Data da solicitação: ${partesData[2]}/${partesData[1]}/${partesData[0]}`;

    const link = document.createElement('a');
    link.textContent = 'Ver detalhes';
    link.href =
      `${window.location.origin}${url_atual}${item.id}/`;

    card.append(titulo, data, link)
    div_items.append(card);
  })
}

// Caso não seja recebido o parametro para new status, mantém o status atual
function carregarPagina(numeroDaPagina, newStatus) {
  fetch(`/manager/api_resp_ugai/?status=${newStatus}&page=${numeroDaPagina}`, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
    console.log('API Response:', data);
    render_items(data.objs);
    console.log(data.objs);
    currentStatus = newStatus;

    paginaAtual = data.currentPage;
    infoPaginaSpan.textContent =
      `Página ${data.currentPage} de ${data.totalPages}`;

  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });
}

btnAnterior.addEventListener('click', () => {
  carregarPagina(paginaAtual - 1);
});

btnProximo.addEventListener('click', () => {
  carregarPagina(paginaAtual + 1);
});

document.addEventListener('DOMContentLoaded', () => {
  currentIcon(1);
  carregarPagina(paginaAtual, 'PENDENTE');
});