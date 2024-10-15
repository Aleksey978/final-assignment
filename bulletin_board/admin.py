from django.contrib import admin
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from .models import Category, Author, PostCategory, Post, Comment, Newsletter


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline]


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'send_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=obj.send_at.minute,
            hour=obj.send_at.hour,
            day_of_month=obj.send_at.day,
            month_of_year=obj.send_at.month,
        )
        PeriodicTask.objects.create(
            crontab=schedule,
            name=obj.subject,
            task='bulletin_board.tasks.send_newsletter',
            args=[obj.id],
        )

admin.site.register(Newsletter, NewsletterAdmin)