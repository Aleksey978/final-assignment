from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, send_mail
from .models import Comment

from django.conf import settings

from_email = settings.DEFAULT_FROM_EMAIL

# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(post_save, sender=Comment)
def notify_managers_appointment(sender, instance, created, **kwargs):
    send_mail(
        subject=f'Пользователь {instance.created_by} оставил отклик',
        # имя клиента и дата записи будут в теме для удобства
        message=f'На вашу запись "{instance.post.title}" оставил отклик: "{instance.text}"',  # сообщение с кратким описанием проблемы
        from_email=from_email,  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        recipient_list=[instance.author.user.email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
    )
    # print(instance.author.user.email)
    # print(created)
    # print(**kwargs)
