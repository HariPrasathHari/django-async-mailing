import time

from celery import shared_task
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from mysite.core.models import Outbox, SentMail


# run this command in the alternative terminal
# celery -A mysite worker -l info


@shared_task
def send_some_mail(delay):
    total = 10
    x = 0
    connection = mail.get_connection()
    connection.open()

    if delay is None:
        delay = 0
    for i in range(total):

        try:
            qs = Outbox.objects.first()
            try:
                mail1 = EmailMultiAlternatives(
                    subject=qs.subject + str(i),
                    body=qs.body + str(i),
                    from_email=qs.fromEmail,
                    to=[qs.toEmail],
                    connection=connection
                )
                mail1.send()

                x = i
                SentMail.objects.create(fromEmail=qs.fromEmail, toEmail=qs.toEmail, body=qs.body, subject=qs.subject,
                                sentTime=timezone.now())
                time.sleep(int(delay))
                qs.delete()

            except Exception as e:
                print(e)
                mail_err = EmailMultiAlternatives(
                    subject='error' + str(i),
                    body=str(e) + str(i),
                    from_email=qs.fromEmail,
                    to=['hariprasathhari9292@gmail.com'],
                    connection=connection
                )
                mail_err.send()
                Outbox.objects.create(fromEmail=qs.fromEmail, toEmail=qs.toEmail, body=qs.body, subject=qs.subject,
                            queuedTime=timezone.now())
                qs.delete()
                pass

        except Exception as e:
            connection.close()
            return '{} Mail sent !\n'.format(x) + str(e)
            pass
    connection.close()
    return '{} Mail sent !\n'.format(x)
