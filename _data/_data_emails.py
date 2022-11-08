# -*- coding: utf-8 -*-
import smtplib
from datetime import datetime
from django.utils.encoding import force_str

import logging

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class email(models.Model):
    email_id = models.BigAutoField(primary_key=True, verbose_name="Email ID")
    email_sender = models.CharField(max_length=250, verbose_name="Email Sender", default=settings.EMAIL_HOST_USER)
    email_receiver = models.CharField(max_length=250, verbose_name="Email Receiver", null=True, blank=True)
    email_title = models.CharField(max_length=250, verbose_name="Email Title", null=True, blank=True)
    email_message = models.CharField(max_length=250, verbose_name="Email Message", null=False, blank=False)
    sending_time = models.DateTimeField(auto_now=True, verbose_name="Sending time")
    sending_state = models.CharField(max_length=250, verbose_name="Email Status", default='Created')
    email_is_sent = models.BooleanField(default=False, verbose_name="Email Sent ?")

    def __str__(self):
        return force_str(f'{self.email_sender} to - {self.email_receiver}- at {self.sending_time}')

    def send(self):
        print('Sending email through SMTP.')
        _msg = self.sendSMTP()
        self.sending_state = _msg
        self.save()

    def sendSMTP(self):
        if self.email_receiver != '':
            try:
                print('# start Sending email through SMTP.')
                start_time = datetime.now()
                message_html_body = self.getMessageRended()
                message_plain_text_body = self.email_message
                res = send_mail(subject=self.email_title, message=message_plain_text_body,
                                from_email=self.email_sender,
                                recipient_list=[self.email_receiver, ], html_message=message_html_body,
                                fail_silently=False)

                time_elapsed = datetime.now() - start_time
                print(f'# res of Sending email through SMTP ---> {res}')
                if res > 0:
                    self.email_is_sent = True
                    return f'MESSAGE SEND RESULT = [YES with SMTP],  SEND TIME=[{time_elapsed}])'
                else:
                    return f'MESSAGE SEND RESULT = [No with SMTP])'
            except smtplib.SMTPException:
                return f'Email not sent due to a SMTP error.'
        else:
            return f'The receiver has no email address !'

    def getMessageRended(self):
        res = ''
        res += '<html>'
        res += '<h3>Email from the uKKU2 quality management system.</h3>'
        res += f'<p>Hello,</p>'
        res += f'<p>{self.email_message}</p>'
        res += f'<p>You received this message because the quality committee in ' \
               f'your college listed you in the uKKU2 users.</p>'
        res += f'<p>Best Regards.</p>'
        res += f'<p>--------- ' \
               f'<br>uKKU2 team - 2022' \
               f'<br>Computer Science Department' \
               f'<br>College of Science and Arts in Tanumah' \
               f'<br>King Khalid University</p>'
        res += '</html>'
        return res

    class Meta:
        ordering = ['email_receiver', 'sending_time']
        verbose_name_plural = "Emails"
        verbose_name = "Email"
        indexes = [
            models.Index(fields=['email_sender', ]),
            models.Index(fields=['email_receiver', ]),
            models.Index(fields=['sending_state', ])
        ]
