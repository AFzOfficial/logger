from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Log(models.Model):
    user = models.ForeignKey(
        User, related_name="logs",
        on_delete=models.CASCADE
        )

    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='log_like', blank=True)

    replay = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)


    def number_of_likes(self):
        return self.likes.count()
    
    def get_all_replies(self):
        return self.replies.all()
    

    def __str__(self):
        return (
            f'{self.user.username} '
            f'{self.created_at} '
            f'{self.body}...'
            )




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=70, null=True, blank=True)


    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True,
    )

    photo = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.user.username



# Auto Create Profile on Create New User
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


# post_save.connect(create_profile, sender=User)