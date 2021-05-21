from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class SendForm(forms.Form):
    email = forms.EmailField(required=True, label="Email")

    def send(self, results):
        email = self.cleaned_data.get('email')
        message = render_to_string('email.html', {'results': results})
        send_mail(
            subject="Resultado da pesquisa sobre inclusão",
            message=message,
            html_message=message,
            recipient_list=[email],
            from_email=settings.DEFAULT_FROM_EMAIL
        )