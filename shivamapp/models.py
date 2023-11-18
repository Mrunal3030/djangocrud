from django.db import models
from django.contrib.auth.models import User
## to send email notification to post creator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

# Signal to send email notification on post creation
@receiver(post_save, sender=Post)
def send_post_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New Post Created'
        message = f'Your new post "{instance.title}" has been created.'
        from_email = 'mrunalvanmale12@gmail.com'  # Replace with your email address
        to_email = [instance.author.email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)
        print(to_email,"())())")




@receiver(post_save, sender=Post)
def send_post_update_email(sender, instance, created, **kwargs):
    if not created:  # Send email only on update, not on create
        subject = f"Post Updated: {instance.title}"
        message = f'Your new post "{instance.title}" has been created.'
        from_email = 'mrunalvanmale12@gmail.com'  # Change this to your email address
        to_email = [instance.author.email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)


@receiver(post_delete, sender=Post)
def send_post_delete_email(sender, instance, **kwargs):
    subject = f"Post Deleted: {instance.title}"
    message = f'Your  post "{instance.title}" has been deleted.'
    from_email = 'mrunalvanmale12@gmail.com'  # Change this to your email address
    to_email = [instance.author.email]
    send_mail(subject, message, from_email, to_email, fail_silently=False)