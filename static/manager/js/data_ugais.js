const div_ugais = document.getElementById('resp_ugais');

function mostrar_visitas() {
  Swal.fire({
    title: "Sweet!",
    text: "Modal with a custom image.",
    imageUrl: "https://unsplash.it/400/200",
    imageWidth: 400,
    imageHeight: 200,
    imageAlt: "Custom image",
    position: 'top'
  });
}

const url_atual = '/manager/dados_ugai/';
fetch('/manager/api_data_ugais/', {
  method: 'GET',
})
  .then(response => response.json())
  .then(data => {
    const table_div = document.getElementById('table');

    const table = document.createElement('table');
    table.classList.add("table", "table-bordered", "border-primary");
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');

    const trHead = document.createElement('tr');
    const thNome = document.createElement('th');
    thNome.textContent = 'Nome da UGAI';
    trHead.appendChild(thNome);
    const thCapacidade = document.createElement('th');
    thCapacidade.textContent = 'Capacidade';
    trHead.appendChild(thCapacidade);
    thead.appendChild(trHead);
    table.appendChild(thead);

    data.objs.forEach(item => {
      const tr = document.createElement('tr');
      const tdNome = document.createElement('td');
      tdNome.textContent = item.nome;
      tr.appendChild(tdNome);
      const tdCapacidade = document.createElement('td');
      tdCapacidade.textContent = item.total_vagas;
      tr.appendChild(tdCapacidade);
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    table_div.appendChild(table);
  })
  .catch(error => {
    console.log('Error fetching data:', error);
  });