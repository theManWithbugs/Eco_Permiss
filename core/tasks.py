from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email(email, mensagem_texto, mensagem_html, subject):

    #subject = Assunto do email
    #message = Texto simples sem formatação caso o texto com html não execute
    #from_email = Remetente
    #fail_silently = Falhar silenciosamente
    #html_message = mensagem de texto com html

    send_mail(
        subject=subject,
        message=mensagem_texto,  # Versão em texto simples
        from_email="wilianaraujo407@gmail.com",
        recipient_list=[email],
        fail_silently=False,
        html_message=mensagem_html
    )
