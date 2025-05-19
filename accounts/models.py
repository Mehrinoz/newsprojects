from django.contrib.auth.models import User
from django.db import models

# class CustumUser(models.Model):
#
#     image = models.ImageField(upload_to='images/',blank=True,null=True)
#     dat_of_birth = models.DateField(blank=True,null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/',blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)

    # class Meta:
    #     verbose_name ="Profil"

    def __str__(self):
        return f"{self.user.username} profili "