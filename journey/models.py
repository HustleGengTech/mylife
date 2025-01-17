from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import magic


#not secure
ext_validator = FileExtensionValidator(['jpeg','pdf','png']) 

#creating variables for image validation using python magic
def validate_image(file):
    accept = ['image/jpeg','application/pdf','image/png']
    image_type = magic.from_buffer(file.read(1024), mime=True)
    if image_type not in accept:
        raise ValidationError('unsupported type')


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 

class DocumentImage(models.Model):
    document = models.ForeignKey(Document, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='documents/',validators=[ext_validator,validate_image])

    def __str__(self):
        return f"Image for {self.document.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True, upload_to='profile_pics')
    profile_bio = models.CharField(null=True,blank=True,max_length=500)
    first_name = models.CharField(null=True,blank=True,max_length=100)
    last_name = models.CharField(null=True,blank=True,max_length=100)
    house_address = models.CharField(null=True,blank=True,max_length=100)
    phone_number = models.CharField(null=True,blank=True,max_length=100)
    city = models.CharField(null=True,blank=True,max_length=100)
    state = models.CharField(null=True,blank=True,max_length=100)
    country = models.CharField(null=True,blank=True,max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'MALE'), ('F', 'FEMALE'), ('O', 'Other')], default='O')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class EmergencyContact(models.Model):
    RELATIONSHIP_CHOICES = [
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('friend', 'Friend'),
        ('co_worker', 'Co-Worker'),
        ('business_partner', 'Business Partner'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.relationship}'
    

#user automatically getting profile
def create_profile(sender,instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
post_save.connect(create_profile,sender=User)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"