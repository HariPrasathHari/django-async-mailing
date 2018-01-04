from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from .forms import SetDelayForm
from .tasks import send_some_mail
from .models import *


class SentMailView(ListView):
    template_name = 'core/sent.html'
    model = SentMail


class OutboxView(ListView):
    template_name = 'core/sent.html'
    model = Outbox


class SetDelayFormView(FormView):
    template_name = 'core/set_delay_email.html'
    form_class = SetDelayForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        send_some_mail.delay(total)
        messages.success(self.request, 'set delay')
        return redirect('sent_mail')
