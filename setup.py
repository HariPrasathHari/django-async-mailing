import hashlib

from django.utils import timezone
from django.utils.crypto import random

from mysite.core.models import *

N = 10  #set N
fromEmail = 'k.a.swetha850@gmail.com'   # set email  to be generated
toEmail = 'hariprasathhari9292@gmail.com'   #to email only for testing
Outbox.objects.all().delete()
SentMail.objects.all().delete()

for i in range(N):
    unique_id = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    Outbox.objects.create(fromEmail=fromEmail, toEmail=toEmail, body=unique_id+' '+str(i), subject=unique_id+' '+str(i),
                          queuedTime=timezone.now())
    unique_id = ''
    pass

'''


'''
