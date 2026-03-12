from .tasks import send_email

def format_data_br(data):
  data = data.split('-')

  data = f"{data[2]}/{data[1]}/{data[0]}"

  return data

def check_number(phone):
  DDD = str(f"({phone[:2]})")
  number = str(phone[2:])

  result = str(DDD + number)
  print(result)

def validador_cpf(cpf):
  numeros = [int(digito) for digito in cpf if digito.isdigit()]

  if len(numeros) != 11:
      return False

  soma1 = sum(a * b for a, b in zip(numeros[0:9], range(10, 1, -1)))
  digito1 = (soma1 * 10 % 11) % 10
  if numeros[9] != digito1:
      return False

  soma2 = sum(a * b for a, b in zip(numeros[0:10], range(11, 1, -1)))
  digito2 = (soma2 * 10 % 11) % 10
  if numeros[10] != digito2:
      return False

  return True

def calcular_data(data_inicio, data_final):

  data_inicio = data_inicio.split('-')
  data_final = data_final.split('-')

  qnt_anos = int(data_final[0]) - int(data_inicio[0])
  qnt_meses = int(data_final[1]) - int(data_inicio[1])

  if qnt_meses == 0:
    ano_txt = "ano" if qnt_anos == 1 else "anos"
    duracao = f"Duração de: {qnt_anos} {ano_txt}"
  else:
    ano_txt = "ano" if qnt_anos == 1 else "anos"
    mes_txt = "mês" if qnt_meses == 1 else "meses"
    duracao = f"Duração de: {qnt_anos} {ano_txt} e {qnt_meses} {mes_txt}"

  return duracao

def email_pesq_aprov(email):
    url = "http://127.0.0.1:8000/user/minhas_solic_pesq/"

    mensagem_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f4f6f8;">

        <div style="max-width:600px; margin:40px auto; background:#ffffff;
                    padding:30px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">

            <h2 style="color:#27ae60; text-align:center;">
                Solicitação de Pesquisa Aprovada
            </h2>

            <p style="font-size:16px;">
                Olá,
            </p>

            <p style="font-size:16px;">
                Informamos que sua <strong>solicitação de pesquisa</strong> foi analisada
                e <strong>aprovada com sucesso</strong> pelo gestor responsável.
            </p>

            <div style="background:#eafaf1; padding:15px; border-radius:6px;
                        border-left:5px solid #27ae60; margin:20px 0;">
                Sua pesquisa já pode ser iniciada. Todas as informações e o acompanhamento
                da solicitação podem ser feitos pelo sistema de gestão.
            </div>

            <div style="text-align:center; margin:25px 0;">
                <a href="{url}"
                   style="background:#2c3e50; color:#ffffff; padding:12px 25px;
                          text-decoration:none; border-radius:5px; font-weight:bold;">
                   Acessar minhas solicitações
                </a>
            </div>

            <p style="font-size:15px;">
                Atenciosamente,<br>
                <strong>Equipe de Gestão de UCs</strong>
            </p>

            <hr style="margin-top:30px; border:none; border-top:1px solid #eee;">

            <p style="font-size:12px; color:#888; text-align:center;">
                Este é um e-mail automático. Por favor, não responda esta mensagem.
            </p>

        </div>

    </body>
    </html>
    """

    mensagem_texto = f"""
    Olá,

    Informamos que sua solicitação de pesquisa foi aprovada com sucesso pelo gestor responsável.

    Sua pesquisa já pode ser iniciada.

    Acompanhe sua solicitação pelo sistema:
    {url}

    Atenciosamente,
    Equipe de Gestão de UCs

    Este é um e-mail automático. Por favor, não responda.
    """

    subject = "Solicitação de pesquisa aprovada"

    send_email.delay(email, mensagem_texto, mensagem_html, subject)

def email_ugai_aprov(email):
    url = "http://127.0.0.1:8000/user/minhas_solic_ugai/"

    mensagem_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f4f6f8;">

        <div style="max-width:600px; margin:40px auto; background:#ffffff;
                    padding:30px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">

            <h2 style="color:#27ae60; text-align:center;">
                Solicitação para uso de UGAI Aprovada
            </h2>

            <p style="font-size:16px;">
                Olá,
            </p>

            <p style="font-size:16px;">
                Informamos que sua <strong>solicitação para utilização de UGAI</strong>
                foi analisada e <strong>aprovada pelo gestor responsável</strong>.
            </p>

            <div style="background:#eafaf1; padding:15px; border-radius:6px;
                        border-left:5px solid #27ae60; margin:20px 0;">
                Caso seja necessário consultar informações como prazo de residência
                ou detalhes da solicitação, elas podem ser verificadas diretamente
                no sistema.
            </div>

            <div style="text-align:center; margin:25px 0;">
                <a href="{url}"
                   style="background:#2c3e50; color:#ffffff; padding:12px 25px;
                          text-decoration:none; border-radius:5px; font-weight:bold;">
                   Acessar minhas solicitações
                </a>
            </div>

            <p style="font-size:15px;">
                Atenciosamente,<br>
                <strong>Equipe de Gestão de UGAIs</strong>
            </p>

            <hr style="margin-top:30px; border:none; border-top:1px solid #eee;">

            <p style="font-size:12px; color:#888; text-align:center;">
                Este é um e-mail automático. Por favor, não responda esta mensagem.
            </p>

        </div>

    </body>
    </html>
    """

    mensagem_texto = f"""
        Olá,

        Informamos que sua solicitação para uso de UGAI foi aprovada com sucesso.

        Você pode consultar detalhes da solicitação e o prazo de residência no sistema:
        {url}

        Atenciosamente,
        Equipe de Gestão de UGAIs

        Este é um e-mail automático. Por favor, não responda.
        """

    subject = "Solicitação para uso de UGAI aprovada"

    send_email.delay(email, mensagem_texto, mensagem_html, subject)

def email_recus_pesq(email, motivo):
    url = "http://127.0.0.1:8000/user/minhas_solic_pesq/"

    mensagem_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color:#f4f6f8;">

        <div style="max-width:600px; margin:40px auto; background:#ffffff;
                    border-radius:8px; padding:30px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">

            <h2 style="color:#c0392b; text-align:center;">
                Solicitação de Pesquisa Recusada
            </h2>

            <p style="font-size:16px;">
                Olá,
            </p>

            <p style="font-size:16px;">
                Informamos que sua <strong>solicitação de autorização para pesquisa</strong> foi analisada e infelizmente <strong>não foi aprovada</strong>.
            </p>

            <div style="background:#f8d7da; padding:15px; border-radius:6px;
                        border-left:5px solid #c0392b; margin:20px 0;">
                <strong>Motivo da recusa:</strong>
                <p style="margin-top:8px;">
                    {motivo}
                </p>
            </div>

            <p style="font-size:15px;">
                Caso deseje consultar ou realizar nova solicitação, acesse o sistema pelo botão abaixo:
            </p>

            <div style="text-align:center; margin:25px 0;">
                <a href="{url}"
                   style="background:#2c3e50; color:#ffffff; padding:12px 25px;
                          text-decoration:none; border-radius:5px; font-weight:bold;">
                   Acessar minhas solicitações
                </a>
            </div>

            <p style="font-size:15px;">
                Atenciosamente,<br>
                <strong>Equipe de Gestão de UCs</strong>
            </p>

            <hr style="margin-top:30px; border:none; border-top:1px solid #eee;">

            <p style="font-size:12px; color:#888; text-align:center;">
                Este é um e-mail automático. Por favor, não responda esta mensagem.
            </p>

        </div>

    </body>
    </html>
    """

    mensagem_texto = f"""
        Olá,

        Informamos que sua solicitação de autorização para pesquisa foi recusada.

        Motivo da recusa:
        {motivo}

        Acesse o sistema para verificar suas solicitações:
        {url}

        Atenciosamente,
        Equipe de Gestão de UCs

        Este é um e-mail automático. Por favor, não responda.
        """

    subject = "Solicitação de pesquisa recusada"

    send_email.delay(email, mensagem_texto, mensagem_html, subject)

    return

def email_recus_ugai(email, motivo):
    url = "http://127.0.0.1:8000/user/minhas_solic_ugai/"

    mensagem_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color:#f4f6f8;">

        <div style="max-width:600px; margin:40px auto; background:#ffffff;
                    border-radius:8px; padding:30px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">

            <h2 style="color:#c0392b; text-align:center;">
                Solicitação de uso de UGAI Recusada
            </h2>

            <p style="font-size:16px;">
                Olá,
            </p>

            <p style="font-size:16px;">
                Informamos que sua <strong>solicitação de autorização para uso de UGAI</strong> foi analisada e infelizmente <strong>não foi aprovada</strong>.
            </p>

            <div style="background:#f8d7da; padding:15px; border-radius:6px;
                        border-left:5px solid #c0392b; margin:20px 0;">
                <strong>Motivo da recusa:</strong>
                <p style="margin-top:8px;">
                    {motivo}
                </p>
            </div>

            <p style="font-size:15px;">
                Caso deseje consultar ou realizar nova solicitação, acesse o sistema pelo botão abaixo:
            </p>

            <div style="text-align:center; margin:25px 0;">
                <a href="{url}"
                   style="background:#2c3e50; color:#ffffff; padding:12px 25px;
                          text-decoration:none; border-radius:5px; font-weight:bold;">
                   Acessar minhas solicitações
                </a>
            </div>

            <p style="font-size:15px;">
                Atenciosamente,<br>
                <strong>Equipe de Gestão de UGAIs</strong>
            </p>

            <hr style="margin-top:30px; border:none; border-top:1px solid #eee;">

            <p style="font-size:12px; color:#888; text-align:center;">
                Este é um e-mail automático. Por favor, não responda esta mensagem.
            </p>

        </div>

    </body>
    </html>
    """

    mensagem_texto = f"""
        Olá,

        Informamos que sua solicitação de autorização para uso de UGAI foi recusada.

        Motivo da recusa:
        {motivo}

        Acesse o sistema para verificar suas solicitações:
        {url}

        Atenciosamente,
        Equipe de Gestão de UGAIs

        Este é um e-mail automático. Por favor, não responda.
        """

    subject = "Solicitação de uso de UGAI Recusada"

    send_email.delay(email, mensagem_texto, mensagem_html, subject)

    return