from celery import shared_task
from django.core.mail import send_mail

@shared_task
def enviar_email(email, mensagem):

    send_mail(
        "Mensagem do sistema",
        mensagem,
        "wilianaraujo407@gmail.com",
        [email],
        fail_silently=False
    )