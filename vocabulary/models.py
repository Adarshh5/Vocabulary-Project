from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from datetime import timedelta
from django.utils.timezone import now

# Create your models here.

class Word(models.Model):
    word_name = models.CharField(max_length=255)
    definition = models.TextField()
    part_of_speech = models.CharField(max_length=30, choices=[
        ('Verb', 'Verb'),
        ('Phrasal Verb', 'Phrasal Verb'),
        ('Adjective', 'Adjective'),
        ('Noun', 'Noun'),
        ('Adverb', 'Adverb'),
        ('Prepostion', 'Prepostion'),

    ])
    example = models.TextField(null=True, blank=True)
    hindi_meaning = models.CharField(max_length=255,null=True,blank=True)
    Synonyms = models.CharField(max_length=255,null=True,blank=True)
    image = CloudinaryField('image')
    level = models.CharField(max_length=30, null=True, choices=[
        ('Basic', 'Basic'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),      
    ])
    
    class Meta:
        unique_together = ['word_name', 'part_of_speech'] 

    def __str__(self):
        return self.word_name


class UserSessionData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    data = models.JSONField(default=dict) 
    updated_at = models.DateTimeField(auto_now=True)  



class UserApiMode(models.Model):
    ACTIVE = 'Active'
    DEACTIVE = 'Deactive'
    API_MODE_CHOICES = [(ACTIVE, 'Active'),(DEACTIVE, 'Deactive'), ]
    user = models.OneToOneField( User, on_delete=models.CASCADE)
    api_mode = models.CharField(max_length=8,choices=API_MODE_CHOICES,default=DEACTIVE )

    

    def __str__(self):
        return f"{self.user.username} - {self.api_mode}"
    

class UserApiPlan(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE )
    api_plan = models.CharField(max_length=50)
    duration_in_days = models.PositiveIntegerField()
    activating_time = models.DateTimeField(default=now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0
    )
    @property
    def end_time(self):
       
        return self.activating_time + timedelta(days=self.duration_in_days)

    def is_expired(self):
        return now() > self.end_time
    
    def __str__(self):
        return f"{self.user.username} - {self.api_plan}"


class UserIdentity(models.Model):
    user = models.OneToOneField( User,on_delete=models.CASCADE)
    identity = models.CharField(max_length=10,unique=True)
    def __str__(self):
        return f"{self.user.username} - {self.identity}"





class OfflineCoaching(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coaching_institute_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='coaching_institutes', null=True, blank=True, default='default.png')
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15) 
    duration = models.CharField(max_length=30,choices=[('1 month', '1 month'),( '3 months', '3 months'), ( '6 months', '6 months'), ( '1 Year', '1 Year')])  
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    MODE_CHOICES = [('Active', 'Active'),('Deactive', 'Deactive'), ]
    status = models.CharField(max_length=20,choices=MODE_CHOICES, default='Deactive')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.coaching_institute_name

    class Meta:
        ordering = ['coaching_institute_name']
        verbose_name = "Offline Coaching"
        verbose_name_plural = "Offline Coachings"