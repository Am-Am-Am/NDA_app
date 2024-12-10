from django import forms
from .models import ContactFormModel

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactFormModel
        fields = ['name', 'email', 'message']