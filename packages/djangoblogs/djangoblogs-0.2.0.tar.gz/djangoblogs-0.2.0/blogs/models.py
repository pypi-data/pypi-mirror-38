from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Post(models.Model):
    uuid = models.UUIDField(primary_key=True)
    author = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, null=True)
    heading = models.CharField(max_length=512, null=True)
    content = models.TextField(null=True)
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    published_on = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self): # pragma: no cover
        return self.slug

    class Meta:
        get_latest_by = '-published_on'
        ordering = ('-published_on', '-created_on')


class Author(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True)
    is_author = models.BooleanField(default=False)

    def __str__(self): # pragma: no cover
        return self.user.username

class Upvote(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    fingerprint = models.CharField(max_length=128)
    is_upvoted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): # pragma: no cover
        return "{}:{}".format(
            self.post.slug,
            self.fingerprint
        )

    class Meta:
        unique_together = ('post', 'fingerprint')
        ordering = ('-created_at',)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create an author on user creation
    """
    if created:
        Author.objects.create(user=instance)
    instance.author.save()
