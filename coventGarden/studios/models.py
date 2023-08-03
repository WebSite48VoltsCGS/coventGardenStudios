from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from .fields import *

# Create your models here.
"""
Account
    - CustomUser
    - CustomGroup
"""
class CustomUser(AbstractUser):
    username = MODEL_USERNAME
    email = MODEL_EMAIL
    last_name = MODEL_LAST_NAME
    first_name = MODEL_FIRST_NAME
    phone = MODEL_PHONE
    password = MODEL_PASSWORD
    password_confirm = MODEL_PASSWORD_CONFIRM
    # is_active = False by default when creating an account using the UserSignUpForm
    # my_groups (See CustomGroup)

    def __str__(self):
        return self.username

class CustomGroup(models.Model):
    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='my_groups'
    )
    name = MODEL_GROUP_NAME
    email = MODEL_GROUP_EMAIL
    phone = MODEL_GROUP_PHONE
    members = MODEL_MEMBERS
    genre = MODEL_GENRE
    facebook = MODEL_FACEBOOK
    instagram = MODEL_INSTAGRAM
    biography = MODEL_BIOGRAPHY
    technical_sheet = MODEL_TECHNICAL_SHEET
    logo = MODEL_LOGO
    validated = MODEL_VALIDATED

    def __str__(self):
        return f"{self.name}"





"""
Booking
    - Event
    - Salle
    - Reservation
"""
class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, default='Untitled Event')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    recurrence = models.CharField(max_length=200, blank=True)
    date = models.DateField(default=timezone.now)

class Salle(models.Model):
    name = models.fields.CharField(max_length=100)
    description = models.fields.CharField(max_length=1000)

    def __str__(self):
        return f'{self.name}'

class Reservation(models.Model):
    class Status(models.TextChoices):
        RESERVED = 'Reserver'
        INPROGRESS = 'En cours'

    # title = models.fields.CharField(default='Item', max_length=100)
    description = models.fields.CharField(max_length=1000)
    duration = models.fields.IntegerField(validators=[MinValueValidator(1)])
    date_start = models.DateTimeField(null=False)
    date_end = models.DateTimeField(null=False)
    price = models.fields.IntegerField(validators=[MinValueValidator(0)])
    status = models.fields.CharField(choices=Status.choices, max_length=20)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=False)
    session_id = models.fields.CharField(max_length=100, null=True)





"""
Pro Area
    - Concert
"""
class Concert(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    groupe1 = models.ForeignKey(CustomGroup, on_delete=models.CASCADE, related_name='concerts_groupe1', null=True)
    groupe2 = models.ForeignKey(CustomGroup, on_delete=models.CASCADE, related_name='concerts_groupe2', null=True)
    groupe3 = models.ForeignKey(CustomGroup, on_delete=models.CASCADE, related_name='concerts_groupe3', null=True)
    date = models.DateField()
    validated = models.BooleanField(default=False)
    planning = models.OneToOneField(Event, on_delete=models.SET_NULL, blank=True, null=True)





"""
Payment
"""
class UserPayment(models.Model):
    app_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)


@receiver(post_save, sender=CustomUser)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(app_user=instance)


#création freefriday

@receiver(post_save, sender=Concert)
def create_event(sender, instance, created, **kwargs):
    if instance.validated:
        description = f"FreeFriday en présence du groupe {instance.groupe1}, du groupe {instance.groupe2} et du groupe {instance.groupe3}"
        date = instance.date  # Supposons que `date` est la date du concert

        Event.objects.update_or_create(
             user=instance.user,
            title='FreeFriday',
            defaults={
                    'date': date,
                    'start_time': date + timedelta(hours=20, minutes=30),
                    'end_time': date + timedelta(hours=23, minutes=30),
                    'description': description
    }
)
        
