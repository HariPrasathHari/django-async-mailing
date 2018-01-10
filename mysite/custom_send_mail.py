from django.utils import timezone

from mysite.core.models import Outbox, EmailCounter
from mysite.core.tasks import send_some_mail
from mysite.settings import DELAY


def get_celery_worker_status():
    ERROR_KEY = "ERROR"
    try:
        from celery.task.control import inspect
        insp = inspect()
        d = insp.stats()
        if not d:
            d = {ERROR_KEY: 'No running Celery workers were found.'}
    except IOError as e:
        from errno import errorcode
        msg = "Error connecting to the backend: " + str(e)
        if len(e.args) > 0 and errorcode.get(e.args[0]) == 'ECONNREFUSED':
            msg += ' Check that the RabbitMQ server is running.'
        d = {ERROR_KEY: msg}
    except ImportError as e:
        d = {ERROR_KEY: str(e)}
    return d


def delayed_send_mail(wait_time):
    stat = get_celery_worker_status()
    print(stat)
    try:
        x = send_some_mail(delay=wait_time)
        print(x)
        err = stat['ERROR']
        print(err)

        y = send_some_mail(delay=wait_time)
        print(y)

    except Exception as e:
        # TODO call the celery shell
        pass


def send_custom_mail(subject, body, recipient_list):
    # todo validate recipient list
    my_mail = ''
    print(subject, body, recipient_list)
    try:
        mail_list = EmailCounter.objects.filter(count__lte=250)
        mmail = mail_list.first()
        my_mail = mmail.from_email
        mmail.count = mmail.count + 1
        mmail.save()
        print(mmail)
    except:
        my_mail = 'gctportal@gmail.com'
        pass
    Outbox.objects.create(
        fromEmail=my_mail,
        toEmail=recipient_list,
        body=body,
        subject=subject,
        queuedTime=timezone.now()
    )
    delayed_send_mail(wait_time=DELAY)
