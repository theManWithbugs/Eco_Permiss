from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.conf import settings

def format_data_br(data):
  data = data.split('-')

  data = f"{data[2]}/{data[1]}/{data[0]}"

  return data

def email_solic_ugai(request, username, ativ_desenv, data_br):
  assunto = "STATUS: Aguardando aprovação"
  texto_simples = "Sua pesquisa foi solicitada com sucesso!"
  destinatarios = ['wilianaraujo407@gmail.com']
  html_content = f"""
  <html>
    <body style="font-family: Arial, sans-serif; color: #333;">

        <h2 style="color:#2c3e50;">
            Autorização para uso de UGAI solicitado com sucesso!
        </h2>

        <p style="font-size: 15px;">
            <strong>Solicitante:</strong> {username}<br>
            <strong>Atividade a desenvolver:</strong> {ativ_desenv}<br>
            <strong>Data da solicitação:</strong> {data_br}
        </p>

        <br>
        <p style="font-size: 14px; color:#555;">
            Atenciosamente<br>
            <strong>SEMA - ECO Permis</strong>
        </p>

    </body>
  </html>
  """

  try:
    email = EmailMultiAlternatives(
            subject=assunto,
            body=texto_simples,
            from_email=settings.EMAIL_HOST_USER,
            to=destinatarios
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
    return True

  except Exception as e:
    messages.error(request, f'ocorreu um erro: {e}')
    return False

def email_solic_ugai(request, username, acao_realizada, data):
  assunto = "STATUS: Aguardando aprovação"
  texto_simples = "Sua pesquisa foi solicitada com sucesso!"
  destinatarios = ['wilianaraujo407@gmail.com']
  html_content = f"""
  <html>
      <body style="font-family: Arial, sans-serif; color: #333;">

          <h2 style="color:#2c3e50;">
              Pesquisa Solicitada com Sucesso!
          </h2>

          <p style="font-size: 15px;">
              <strong>Solicitante:</strong> {username}<br>
              <strong>Ação a ser realizada:</strong> {acao_realizada}<br>
              <strong>Data da solicitação:</strong> {data}
          </p>

          <br>
          <p style="font-size: 14px; color:#555;">
              Atenciosamente<br>
              <strong>SEMA - ECO Permis</strong>
          </p>

      </body>
  </html>
  """
  try:
    email = EmailMultiAlternatives(
          subject=assunto,
          body=texto_simples,
          from_email=settings.EMAIL_HOST_USER,
          to=destinatarios
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return True

  except Exception as e:
    messages.error(request, f'ocorreu um erro: {e}')
    return False

def email_pesq_aprov(request, username):
  assunto = "STATUS: pesquisa aprovada com sucesso!"
  texto_simples = "Sua pesquisa foi aprovada com sucesso!"
  destinatarios = ['wilianaraujo407@gmail.com']
  html_content = f"""
  <html>
      <body style="font-family: Arial, sans-serif; color: #333;">

          <h2 style="color:#2c3e50;">
              Pesquisa aprovada!
          </h2>

          <p style="font-size: 15px;">
              <strong>Gestor responsavel:</strong> {username}<br>
          </p>

          <br>
          <p style="font-size: 14px; color:#555;">
              Atenciosamente<br>
              <strong>SEMA - ECO Permis</strong>
          </p>

      </body>
  </html>
  """
  try:
    email = EmailMultiAlternatives(
          subject=assunto,
          body=texto_simples,
          from_email=settings.EMAIL_HOST_USER,
          to=destinatarios
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return True

  except Exception as e:
    messages.error(request, f'ocorreu um erro: {e}')
    return False

def email_ugai_aprov(request, username):
  assunto = "STATUS: Solicitação para uso de UGAI"
  texto_simples = "Sua solicitação para uso de UGAI foi aprovada com sucesso!"
  destinatarios = ['wilianaraujo407@gmail.com']
  html_content = f"""
  <html>
      <body style="font-family: Arial, sans-serif; color: #333;">

          <h2 style="color:#2c3e50;">
              Uso de ugai aprovado!
          </h2>

          <p style="font-size: 15px;">
              <strong>Gestor responsavel:</strong> {username}<br>
          </p>

          <br>
          <p style="font-size: 14px; color:#555;">
              Atenciosamente<br>
              <strong>SEMA - ECO Permis</strong>
          </p>

      </body>
  </html>
  """
  try:
    email = EmailMultiAlternatives(
          subject=assunto,
          body=texto_simples,
          from_email=settings.EMAIL_HOST_USER,
          to=destinatarios
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    return True

  except Exception as e:
    messages.error(request, f'ocorreu um erro: {e}')
    return False