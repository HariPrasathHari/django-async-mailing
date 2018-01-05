Installation
The easiest way to install Celery is using pip:

pip install Celery


Now we have to install RabbitMQ.

Installing RabbitMQ on Ubuntu 16.04
To install it on a newer Ubuntu version is very straightforward:


apt-get install -y erlang
apt-get install rabbitmq-server



Then enable and start the RabbitMQ service:

systemctl enable rabbitmq-server
systemctl start rabbitmq-server



Check the status to make sure everything is running smooth:



systemctl status rabbitmq-server



start the process by async

celery -A mysite worker -l info



setup.py add test email 
setting.py add email