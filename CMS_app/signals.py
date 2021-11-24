from .models import CustomUser

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.urls import reverse

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import get_template, render_to_string
from .tokens import account_activation_token

# from requests import request

@receiver(post_save, sender=CustomUser)
def SendActivationMail(sender,request, instance, created, **kwargs): 
   if created:  
      current_site = get_current_site(request)
      print("signal started")
      mail_subject = 'Activate your account.'
      user = CustomUser.objects.get(username=instance)
      message = render_to_string('crm/user_account_activation_email.html', {
          'user': user,
          'domain': current_site.domain,
          'uid':urlsafe_base64_encode(force_bytes(user.pk)),
          'token':account_activation_token.make_token(user),
      })
      to_email = user.email
      email = EmailMessage(
                  mail_subject, message, to=[to_email]
      )
      email.send(fail_silently=False)
      print("mail sent by signal")
   