from django.template.loader import render_to_string

from nda_email.temporary_storage import temporary_storage
from nda_email.forms import ContactForm
from nda_email.tasks import send_emails_task


class EmailSender:
    @staticmethod
    def get_message_data(request):
        form = ContactForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Cannot send email, form is invalid')
        customer_email = form.cleaned_data['email']
        customer_phone = form.cleaned_data['phone_number']
        customer_message = form.cleaned_data['message']
        file = request.FILES['company_details'] if 'company_details' in request.FILES else None
        return customer_email, customer_phone, customer_message, file

    @classmethod
    def send_messages(cls, request, offers):
        customer_email, customer_phone, customer_message, file = cls.get_message_data(request)
        context = {
            'customer_message': customer_message,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            }
        if offers != 0:
            context['offers'] = offers
        html_message_for_nda = render_to_string(
                'cart/message_for_nda.html',
                context
            )
        html_message_for_customer = render_to_string(
                'cart/message_for_customer.html',
                context)
        storaged_file = None
        if file is not None:
            storaged_file = temporary_storage.save(file.name, file)
        send_emails_task.delay(html_message_for_nda, html_message_for_customer, customer_email, storaged_file)
