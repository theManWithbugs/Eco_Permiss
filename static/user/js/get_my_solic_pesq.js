
  const container_error = document.getElementById("container_error");
  const div_pesquisas_solic = document.getElementById("pesquisas_solic");

  const target_url = '/user/info_pesquisas/';

  function render_solic_pesq(elements) {
    const header_pesquisas = document.createElement("h4");
    header_pesquisas.textContent = "Pesquisas | (Solicitadas/Finalizadas)";
    header_pesquisas.style = "margin-bottom: 20px; margin-top: 15px;";
    header_pesquisas.classList = "pesquisas_title";
    div_pesquisas_solic.appendChild(header_pesquisas);

    elements.forEach(element => {
      const card = document.createElement("div");
      card.className = "card_items";

      const titulo = document.createElement("h5");
      titulo.textContent = element["acao_realizada"];

      const status = document.createElement("p");
      if (element["status"]) {
        status.textContent = "EM-ANDAMENTO/AGUARDANDO-APROVAÇÃO";
        status.style = "color: blue;";
      } else {
        status.textContent = "INATIVO/FINALIZADO";
        status.style = "color: red;";
    }

      const link = document.createElement("a");
      link.textContent = "Ver detalhes";
      link.href =
        `${window.location.origin}${target_url}${element.id}/`;

      const partesData = element.data_solicitacao.split("-");
      const data = document.createElement("p");
      data.textContent = `Data da solicitação: ${partesData[2]}/${partesData[1]}/${partesData[0]}`;

      card.append(titulo, status, link, data);
      div_pesquisas_solic.appendChild(card);
    })
  }

  fetch(`/user/get_my_solic_pesq/`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      },
    })
    .then(response => response.json())
    .then(data => {
      render_solic_pesq(data.objs);
    })
    .catch(error => {
      container_error.innerHTML = `Erro ao carregar os dados: ${error}`;
    })
