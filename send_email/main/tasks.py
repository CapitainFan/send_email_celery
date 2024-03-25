from django.core.mail import send_mail
from send_email.celery import app
from celery import shared_task
from .service import send
from .models import Contact


@app.task
def send_spam_email(user_email):
    send(user_email)


@app.task
def send_beat_email():
    for contact in Contact.objects.all():
        send_mail(
            'Вы подписались на рассылку',
            'Мы будем присылать Вам много спама каждые 10 минут.',
            'bossbog18@gmail.com',
            [contact.email],
            fail_silently=False,
        )


@app.task()
def test_task_1():
    print('Worked')
    return True


@app.task()
def test_task_2(a, b):
    c = a + b
    return c
# test_task_2.apply_async((5, 5), link=test_task_2.s(20))


@app.task(bind=True, default_retry_delay=5*60)
def test_task_3(self, x, y):
    try:
        return x + y
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
# test_task_3.apply_async(countdown=60)


@shared_task()
def test_sh_task(msg):
    return msg + '!!!'
