from django.db import models
from django.conf import settings


class Post(models.Model):
    creator                     = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='posts',
                                    on_delete=models.CASCADE)
    
    content                  = models.CharField(max_length=200000)
    likes                    = models.IntegerField(default=0)
    users_who_liked          = models.ManyToManyField(settings.AUTH_USER_MODEL)
    date_created                  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_created',)


    
