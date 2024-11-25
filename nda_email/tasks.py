from datetime import datetime
from celery import shared_task

from django.core.mail import EmailMessage

from NDA_app.settings import EMAIL_HOST_USER, RECIPIENT_EMAIL
from nda_email.temporary_storage import temporary_storage


@shared_task
def send_emails_task(html_message_for_nda, html_message_for_customer, customer_email, file_name):
    subject_for_nda = f'Заказ с сайта от {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
    email_for_nda = EmailMessage(subject_for_nda,
                                 html_message_for_nda, EMAIL_HOST_USER, [RECIPIENT_EMAIL])
    subject_for_customer = f'Ваш заказ от {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
    email_for_customer = EmailMessage(subject_for_customer,
                                      html_message_for_customer, EMAIL_HOST_USER, [customer_email])
    if file_name is not None:
        storaged_file_path = temporary_storage.path(file_name)
        email_for_nda.attach_file(storaged_file_path)
        email_for_customer.attach_file(storaged_file_path)
        temporary_storage.delete(file_name)
    email_for_nda.send(fail_silently=False)
    email_for_customer.send(fail_silently=False)
