from django.utils import timezone

from mysite.core.models import Outbox
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
    try:
        err = stat['ERROR']
        # call another thread celery
        send_some_mail(delay=wait_time)


    except Exception as e:
        # TODO call the celery shell
        # no workers running
        pass


def send_custom_mail(subject, body, from_email, recipient_list):
    # todo validate recipient list
    Outbox.objects.create(
        fromEmail=from_email,
        toEmail=recipient_list,
        body=body,
        subject=subject,
        queuedTime=timezone.now()
    )
    delayed_send_mail(wait_time=DELAY)
