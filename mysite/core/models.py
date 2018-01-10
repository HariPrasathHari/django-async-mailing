from django.db import models

# Create your models here.


class Outbox(models.Model):
    fromEmail = models.CharField(max_length=100)
    toEmail = models.TextField()
    body = models.TextField(null=True,blank=True)
    subject = models.TextField(null=True,blank=True)
    queuedTime = models.DateTimeField()

    def __str__(self):
        return self.subject


class SentMail(models.Model):
    fromEmail = models.CharField(max_length=100)
    toEmail = models.TextField()
    body = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    sentTime = models.DateTimeField()

    def __str__(self):
        return self.subject


class EmailCounter(models.Model):
    from_email = models.EmailField()
    password = models.CharField(max_length=50)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.from_email + str(self.count)


class MailError(models.Model):
    Error = models.TextField()
    fromEmail = models.CharField(max_length=100)
    toEmail = models.TextField()
    body = models.TextField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    queuedTime = models.DateTimeField()

    def __str__(self):
        return self.Error
