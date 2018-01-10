import time

from celery import shared_task
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from mysite.core.models import EmailCounter
from mysite.core.models import Outbox, SentMail
# run this command in the alternative terminal
# celery -A mysite worker -l info
from mysite.settings import DELAY, SEND_LIMIT


@shared_task
def send_some_mail(delay=DELAY):
    send_limit = SEND_LIMIT
    x = 0
    try:
        queryset = Outbox.objects.first()
        sender = queryset.fromEmail
        newqs = Outbox.objects.filter(fromEmail=sender)
        pass
    except:
        return 'nothing in outbox'
        pass
    connection = mail.get_connection(
        username=sender,
        password=EmailCounter.objects.get(from_email=sender).password,
    )
    connection.open()

    if delay is None:
        delay = 0
    for i in range(send_limit):
        try:
            qs = newqs.first()
            try:
                mail1 = EmailMultiAlternatives(
                    subject=qs.subject,
                    body=qs.body,
                    from_email=qs.fromEmail,
                    to=qs.toEmail.split(','),
                    connection=connection
                )
                mail1.send()

                x = i
                SentMail.objects.create(fromEmail=qs.fromEmail, toEmail=qs.toEmail.split(','), body=qs.body,
                                        subject=qs.subject,
                                        sentTime=timezone.now())
                time.sleep(int(delay))
                qs.delete()

            except Exception as e:
                print(e)
                try:
                    mail_err = EmailMultiAlternatives(
                        subject='error',
                        body=str(e),
                        from_email=qs.fromEmail,
                        to=['hariprasathhari9292@gmail.com'],
                        connection=connection
                    )
                    # todo logging
                    mail_err.send()
                except:
                    pass
                Outbox.objects.create(
                    fromEmail=qs.fromEmail,
                    toEmail=qs.toEmail.split(','),
                    body=qs.body,
                    subject=qs.subject,
                    queuedTime=timezone.now())
                qs.delete()
                pass

        except Exception as e:
            connection.close()
            return '{} Mail sent !\n'.format(x) + str(e)
            pass
    connection.close()
    return '{} Mail sent !\n'.format(x)
