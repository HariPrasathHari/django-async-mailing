from django.db import models

# Create your models here.


class Outbox(models.Model):
    fromEmail = models.CharField(max_length=100)
    toEmail = models.CharField(max_length=100)
    body = models.TextField(null=True,blank=True)
    subject = models.TextField(null=True,blank=True)
    queuedTime = models.DateTimeField()

    def __str__(self):
        return self.subject


class SentMail(models.Model):
    fromEmail = models.CharField(max_length=100)
    toEmail = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    sentTime = models.DateTimeField()

    def __str__(self):
        return self.subject
