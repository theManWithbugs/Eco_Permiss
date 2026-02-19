let currentStatus;
let paginaAtual = 1;

const url_atual = '/manager/info_pesq/';

const div_items = document.getElementById('div_items');
const btnAnterior = document.getElementById('btn-anterior');
const btnProximo = document.getElementById('btn-proximo');
const infoPaginaSpan = document.getElementById('info-pagina');

const pesqInativas = document.getElementById('pesqInativas');
const pesqAtivas = document.getElementById('pesqAtivas');

const div_title = document.getElementById('title_page');
function currentIcon(value) {
  switch (value) {
    case 1:
      pesqAtivas.style.borderColor = 'silver';
      pesqInativas.style.borderColor = 'black';

      div_title.textContent = '(Pesquisas | Inativas-Finalizadas)';
      break;

    case 2:
      pesqInativas.style.borderColor = 'silver';
      pesqAtivas.style.borderColor = 'black';

      div_title.textContent = '(Pesquisas | Ativas-Aguardando)';
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
    titulo.textContent = item.acao_realizada;

    // const status = document.createElement('span');
    // status.innerHTML = `${item.status}`;

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
function carregarPagina(numeroDaPagina, newStatus = currentStatus) {
  fetch(`/manager/api_resp_pesq/?status=${newStatus}&page=${numeroDaPagina}`, {
    method: 'GET',
  })
  .then(response => response.json())
  .then(data => {
    console.log('API Response:', data);
    render_items(data.objs);
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
  carregarPagina(paginaAtual, false);
});
