
# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_mail_template(subject, template_name, context, recipient_list, from_email, fail_silently=False):

    message_html = render_to_string(template_name, context)

    message_txt = striptags(message_html)

    email = EmailMultiAlternatives(
        subject=subject, body=message_txt, from_email=from_email,
        to=recipient_list
    )
    email.attach_alternative(message_html, "text/html")
    email.send(fail_silently=fail_silently)


def send_mail(title, machine, password, user, user_email):
    subject = u"Contato Cloud - {0} Máquina {1}".format(title, machine)
    context = {
        'machine': machine,
        'password': password,
        'user': user,
    }

    template_name = 'contact_email.html'
    send_mail_template(
        subject,
        template_name,
        context,
        [user_email], settings.CONTACT_EMAIL)
