from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.core.validators import MinValueValidator, MaxValueValidator

# **************************************************************************************
# Driver Info
# **************************************************************************************
class Driver(models.Model):
    name=models.CharField(max_length=30,blank=False,null=False,verbose_name='Driver Name')
    
    license_number=models.CharField(max_length=30,blank=False,verbose_name="License Plate Number")
    vehicle_type_choice=(
        ('EC','Basic Economy - Affordable, everyday ride'),
        ('ECXL','Economy XL - Affordable rides for groups up to 5'),
        ('LX','Luxury - High-end and newer cars'),
        ('GR','Green- Eco-friendly'),
        ('PT','Pet - Affordable rides for you and your pet'),
    )
    vehicle_type=models.CharField(max_length=20,choices=vehicle_type_choice,verbose_name="Vehicle Type")
   
    capacity=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],default=1,blank=False,verbose_name="Passenger Capacity")
    special_vehicle_info=models.TextField(blank=True,null=True, verbose_name="Special Vehicle Information")
    user=models.OneToOneField(
        #to=settings.AUTH_USER_MODEL,
        to = User,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (self.name)

    def get_absolute_url(self):
        return reverse('rideshare:driver-detail',kwargs={'pk':self.pk})

# **************************************************************************************
# Ride Request
# **************************************************************************************
class Rides(models.Model):
    request_id=models.AutoField(primary_key=True, verbose_name='Request_id')
    destination=models.CharField(max_length=100,blank=False,verbose_name='Destination')
    arrive_date=models.DateTimeField(blank=False,verbose_name='Request Arrival Date and Time')
    number_passenger=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],default=1,blank=False,verbose_name='Passenger Number')
    share_choice=(
        ('Y','Yes'),
        ('N','No'),
    )
    share=models.CharField(max_length=5,choices=share_choice,verbose_name="Share Ride")
    status_choice=(
        ('OP','Open'),
        ('CF','Confirmed'),
        ('CL','Closed'),
        ('CA','Cancel'),
    )
    status=models.CharField(max_length=20,choices=status_choice,verbose_name="Status")
    vehicle_type_choice=(
        ('EC','Basic Economy - Affordable, everyday ride'),
        ('ECXL','Economy XL - Affordable rides for groups up to 5'),
        ('LX','Luxury - High-end and newer cars'),
        ('GR','Green- Eco-friendly'),
        ('PT','Pet - Affordable rides for you and your pet'),
    )
    vehicle_type=models.CharField(max_length=20,choices=vehicle_type_choice,verbose_name="Vehicle Type")
    special_request=models.TextField(blank=True,null=True,verbose_name="Special Request")
    owner=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    sharer=models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="ride_sharer"
    )
    has_sharer_choice=(
        ('Y','Y'),
        ('N','N'),
    )
    has_sharer=models.CharField(default='N',max_length=5,choices=has_sharer_choice,verbose_name="Has Sharer")
    driver=models.ForeignKey(
        Driver,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="ride_driver"
    )
    def __str__(self):
        return (self.destination)

    def get_absolute_url(self):
        return reverse('rideshare:ride-detail',kwargs={'pk':self.pk})

    def send_email(self):
        subject = "RideShare Update"
        message = "Ride ID: " + str(self.request_id) + " to " + self.destination + " Status: " + self.get_status_display()
        from_email = settings.EMAIL_HOST_USER
        to_email=[self.owner.email]
        for sharer in self.sharer.all():
            to_email.append(sharer.email)
         
        try:
            send_mail(subject, message, from_email, to_email)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return



# **************************************************************************************
# Sharer Search
# **************************************************************************************
class sharer_search(models.Model):
    sharer=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    destination=models.CharField(max_length=100,blank=False,verbose_name='Destination')
    arrive_date_early=models.DateTimeField(blank=False,verbose_name='Request Early Arrival Date and Time')
    arrive_date_late=models.DateTimeField(blank=False,verbose_name='Request Late Arrival Date and Time')
    number_passenger=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)],default=1,blank=False,verbose_name='Passenger Number')
    join_ride=models.IntegerField(default=0,blank=True)
    def get_absolute_url(self):
        return reverse('rideshare:sharer-list')
