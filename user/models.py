from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.utils import timezone
# Create your models here.


class UserProfile(models.Model):

    # faire un field liste  je cree d'abord la liste et je le met coe choix
    MASCULIN = 'M'
    FEMININ = 'F'
    SEXE_CHOICES = [
        (MASCULIN, 'Masculin'),
        (FEMININ, 'Feminin'), ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #phone = models.CharField(max_length= 9)
    image = models.ImageField(blank=True, null=True)
    date_naissance = models.DateField(blank=True)
    genre = models.CharField(
        max_length=1,
        choices=SEXE_CHOICES, blank=True)
    affiliation = models.CharField(max_length=1, blank=False)
    email = models.EmailField(max_length=254, blank=False)

    """
    def delete_user(sender, instance=None, **kwargs):
        try:
            instance.user
        except User.DoesNotExist:
            pass
        else:
            instance.user.delete()
    signals.post_delete.connect(delete_user, sender=UserProfile)
    """


class Code(models.Model):
    code = models.IntegerField(default=0)
    date_create = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    heure = models.TimeField(timezone.now())
