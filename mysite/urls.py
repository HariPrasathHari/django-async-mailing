from django.conf.urls import url

from mysite.core import views


urlpatterns = [

    url(r'^sent$', views.SentMailView.as_view(), name='sent_mail'),
    url(r'^outbox$', views.OutboxView.as_view(), name='outbox_list'),
    url(r'^delaySet$', views.SetDelayFormView.as_view(), name='delaySet'),
    url(r'^$', views.OutboxView.as_view(), name='outbox_list'),
]
