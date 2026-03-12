from core.tasks import send_email

def format_data_br(data):
  data = data.split('-')

  data = f"{data[2]}/{data[1]}/{data[0]}"

  return data


#Funções de enviar email refatoradas
#------------------------------------------------------------------#
#------------------------------------------------------------------#

def email_solic_pesquisa(email, username, acao_realizada, data):
    url = "http://127.0.0.1:8000/user/minhas_solic_pesq/"

    mensagem_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f4f6f8;">

        <div style="max-width:600px; margin:40px auto; background:#ffffff;
                    padding:30px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">

            <h2 style="color:#2980b9; text-align:center;">
                Solicitação de Pesquisa Recebida
            </h2>

            <p style="font-size:16px;">Olá,</p>

            <p style="font-size:15px;">
                Sua solicitação de pesquisa foi <strong>recebida com sucesso</strong> e já está em análise pela gestão responsável.
            </p>

            <div style="background:#eef5fb; padding:15px; border-radius:6px;
                        border-left:5px solid #2980b9; margin:20px 0;">

                <strong>Detalhes da solicitação:</strong><br><br>

                <strong>Solicitante:</strong> {username}<br>
                <strong>Ação a ser realizada:</strong> {acao_realizada}<br>
                <strong>Data da solicitação:</strong> {data}

            </div>

            <p style="font-size:15px;">
                O prazo para avaliação é de até <strong>7 dias úteis</strong>.
                Assim que o processo for concluído, você receberá um novo e-mail com o resultado.
            </p>

            <div style="text-align:center; margin:25px 0;">
                <a href="{url}"
                   style="background:#2c3e50; color:#ffffff; padding:12px 25px;
                          text-decoration:none; border-radius:5px; font-weight:bold;">
                   Acompanhar solicitação
                </a>
            </div>

            <p style="font-size:15px;">
                Atenciosamente,<br>
                <strong>Equipe de Gestão de UCs</strong>
            </p>

            <hr style="margin-top:30px; border:none; border-top:1px solid #eee;">

            <p style="font-size:12px; color:#888; text-align:center;">
                Este é um e-mail automático. Por favor, não responda.
            </p>

        </div>

    </body>
    </html>
    """

    mensagem_texto = f"""
        Solicitação de pesquisa recebida

        Solicitante: {username}
        Ação a ser realizada: {acao_realizada}
        Data da solicitação: {data}

        Sua solicitação foi recebida e está em análise pela gestão responsável.
        O prazo para avaliação é de até 7 dias úteis.

        Acompanhe sua solicitação:
        {url}

        Equipe de Gestão de UCs
        Este é um e-mail automático. Por favor, não responda.
        """

    subject = "Sua solicitação de pesquisa foi recebida"

    send_email.delay(email, mensagem_texto, mensagem_html, subject)

def email_solic_ugai(email, username, ativ_desenv, data_br):
    url = "http://127.0.0.1:8000/user/minhas_solic_ugai/"

    mensagem_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f4f6f8;">

        <div style="max-width:600px; margin:40px auto; background:#ffffff;
                    padding:30px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">

            <h2 style="color:#2980b9; text-align:center;">
                Solicitação de Uso de UGAI Recebida
            </h2>

            <p style="font-size:16px;">Olá,</p>

            <p style="font-size:15px;">
                Sua solicitação para <strong>utilização de UGAI</strong> foi recebida com sucesso
                e já está em análise pela gestão responsável.
            </p>

            <div style="background:#eef5fb; padding:15px; border-radius:6px;
                        border-left:5px solid #2980b9; margin:20px 0;">

                <strong>Detalhes da solicitação:</strong><br><br>

                <strong>Solicitante:</strong> {username}<br>
                <strong>Atividade a desenvolver:</strong> {ativ_desenv}<br>
                <strong>Data da solicitação:</strong> {data_br}

            </div>

            <p style="font-size:15px;">
                O prazo para avaliação é de até <strong>7 dias úteis</strong>.
                Você receberá um novo e-mail assim que a análise for concluída.
            </p>

            <div style="text-align:center; margin:25px 0;">
                <a href="{url}"
                   style="background:#2c3e50; color:#ffffff; padding:12px 25px;
                          text-decoration:none; border-radius:5px; font-weight:bold;">
                   Acompanhar solicitação
                </a>
            </div>

            <p style="font-size:15px;">
                Atenciosamente,<br>
                <strong>Equipe de Gestão de UGAIs</strong>
            </p>

            <hr style="margin-top:30px; border:none; border-top:1px solid #eee;">

            <p style="font-size:12px; color:#888; text-align:center;">
                Este é um e-mail automático. Por favor, não responda.
            </p>

        </div>

    </body>
    </html>
    """

    mensagem_texto = f"""
        Solicitação de uso de UGAI recebida

        Solicitante: {username}
        Atividade a desenvolver: {ativ_desenv}
        Data da solicitação: {data_br}

        Sua solicitação foi recebida e está em análise pela gestão responsável.
        O prazo de avaliação é de até 7 dias úteis.

        Acompanhe sua solicitação:
        {url}

        Equipe de Gestão de UGAIs
        Este é um e-mail automático. Por favor, não responda.
        """

    subject = "Sua solicitação de UGAI foi recebida"

    send_email.delay(email, mensagem_texto, mensagem_html, subject)

def email_equipe_pesq(email, solicitante, id_pesq):
    url = f"http://127.0.0.1:8000/user/conf_email_equip/{id_pesq}/"

    mensagem_html = f"""
    <html>
    <body style="margin:0; padding:0; font-family: Arial, sans-serif; background:#f4f6f8;">

        <div style="max-width:600px; margin:40px auto; background:#ffffff;
                    padding:30px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">

            <h2 style="color:#2980b9; text-align:center;">
                Convite para participar de pesquisa
            </h2>

            <p style="font-size:16px;">
                Olá,
            </p>

            <p style="font-size:15px;">
                Você foi <strong>convidado para participar de uma equipe de pesquisa</strong>
                no sistema de Gestão de UCs.
            </p>

            <div style="background:#eef5fb; padding:15px; border-radius:6px;
                        border-left:5px solid #2980b9; margin:20px 0;">

                <strong>Detalhes do convite:</strong><br><br>

                <strong>Solicitante:</strong> {solicitante}<br>
                <strong>Status:</strong> Aguardando confirmação do membro da equipe

            </div>

            <p style="font-size:15px;">
                Para confirmar sua participação nesta pesquisa, clique no botão abaixo
                e autorize sua inclusão como membro da equipe.
            </p>

            <div style="text-align:center; margin:30px 0;">
                <a href="{url}"
                   style="background:#27ae60; color:#ffffff; padding:14px 28px;
                          text-decoration:none; border-radius:6px; font-weight:bold;
                          font-size:16px;">
                   Confirmar participação
                </a>
            </div>

            <p style="font-size:15px;">
                Caso você não reconheça esta solicitação, basta ignorar este e-mail.
            </p>

            <p style="font-size:15px;">
                Atenciosamente,<br>
                <strong>Equipe de Gestão de UCs</strong>
            </p>

            <hr style="margin-top:30px; border:none; border-top:1px solid #eee;">

            <p style="font-size:12px; color:#888; text-align:center;">
                Este é um e-mail automático. Por favor, não responda.
            </p>

        </div>

    </body>
    </html>
    """

    mensagem_texto = f"""
        Convite para participar de pesquisa

        Você foi convidado por {solicitante} para participar de uma equipe de pesquisa.

        Para confirmar sua participação, acesse o link abaixo:
        {url}

        Caso não reconheça esta solicitação, ignore este e-mail.

        Equipe de Gestão de UCs
        Este é um e-mail automático. Não responda.
        """

    subject = "Convite para participar de equipe de pesquisa"
    send_email.delay(email, mensagem_texto, mensagem_html, subject)

    return