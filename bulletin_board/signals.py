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
        message=f'На вашу запись "{instance.post.title}" оставил отклик: "{instance.text}"',
        from_email=from_email,
        recipient_list=[instance.author.user.email]
    )

@receiver(post_save, sender=Comment)
def perform_action_on_comment_accept(sender, instance, **kwargs):
    if instance.accept and kwargs.get('created', False) is False:
        send_mail(
            subject=f'Ваш отклик {instance.text} приинят автором',
            message=f'Оклик {instance.text} к записи  "{instance.post.title}" принят автором',
            from_email=from_email,
            recipient_list=[instance.created_by.email]
        )
