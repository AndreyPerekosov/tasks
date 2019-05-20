from django.contrib.auth.models import User
from django.db import models
from django import forms

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    # avatar = models.ImageField(upload_to="user_avatars/%Y/%m/%d", blank=True)

    def __str__(self):
        return "Профиль пользователя %s" % self.user.username

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        # fields = ("birthdate", "avatar")
        fields = ("birthdate",)