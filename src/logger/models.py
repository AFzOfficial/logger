from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Log(models.Model):
    user = models.ForeignKey(User, related_name="logs",
                             on_delete=models.CASCADE)

    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_reply = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='like', blank=True)
    replies = models.ManyToManyField('self', related_name='reply', symmetrical=False, blank=True)


    def number_of_likes(self):
        return self.likes.count()

    def number_of_replies(self):
        return self.replies.count()

    def __str__(self):
        return (
            f'{self.user.username} '
            f'{self.body[:20]}...'
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=70, null=True, blank=True)
    premium = models.DateTimeField(default=timezone.now)

    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True,
    )

    photo = models.ImageField(null=True, blank=True, upload_to='images/')


    def is_premium(self) -> bool:
        if self.premium > timezone.now():
            return True
        
        return False


    def __str__(self) -> str:
        return self.user.username


# Auto Create Profile on Create New User
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


# post_save.connect(create_profile, sender=User)
