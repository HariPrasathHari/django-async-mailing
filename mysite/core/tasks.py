from datetime import datetime
import time
from django.utils import timezone

from celery import shared_task
from django.core.mail import send_mail
from .models import Outbox, SentMail

# run this command in the alternative terminal
# celery -A mysite worker -l info


@shared_task
def send_some_mail(delay):
    total = 10
    x = 0
    if  delay==None:
        delay = 0
    for i in range(total):

        try:
            qs = Outbox.objects.first()
            try:
                send_mail(
                    subject=qs.subject + str(i),
                    message=qs.body + str(i),
                    from_email=qs.fromEmail,
                    recipient_list=[qs.toEmail])
                x = i
                SentMail.objects.create(fromEmail=qs.fromEmail, toEmail=qs.toEmail, body=qs.body, subject=qs.subject,
                                sentTime=timezone.now())
                time.sleep(int(delay))
                qs.delete()

            except Exception as e:
                print(e)
                send_mail(
                    subject='error' + str(i),
                    message=str(e) + str(i),
                    from_email=qs.fromEmail,
                    recipient_list=['hariprasathhari9292@gmail.com'])
                Outbox.objects.create(fromEmail=qs.fromEmail, toEmail=qs.toEmail, body=qs.body, subject=qs.subject,
                            queuedTime=timezone.now())
                qs.delete()
                pass

        except Exception as e:
            return '{} Mail sent !\n' + str(e).format(i)
            pass
    return '{} Mail sent !\n' + str(e).format(i)