from django.db import models
import os

# Create your models here.

class userModel(models.Model):
    userID = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100, null=True)
    userEmail = models.EmailField(null=True)
    password = models.CharField(max_length=50, null=True)
    confirmPass = models.CharField(max_length=50, null=True)
    addresh = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=100, null=True)
    profilePic = models.ImageField(upload_to=os.path.join('static', 'userProfile'), default='No Profile')

    def __str__(self):
        return self.userName
    
    class Meta:
        db_table = 'userModel'

class tourPlaces(models.Model):
    placeID = models.AutoField(primary_key=True)
    placeName = models.CharField(max_length=100, null=True)
    placeLocation = models.CharField(max_length=100, null=True)
    Country = models.CharField(max_length=100, null=True)
    placePic = models.ImageField(upload_to=os.path.join('static', 'placePic'), default='No profile')
    description = models.TextField(max_length=1000, null=True)
    price = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.JSONField(default=list,blank=True)
    places = models.JSONField(default=list,blank=True)
    restaurants = models.JSONField(default=list,blank=True)
    placeType = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.placeName
    
    class Meta:
        db_table = 'tourPlaces'

class addFlightsModel(models.Model):
    flightId = models.AutoField(primary_key=True)
    From = models.CharField(max_length=100, null=True)
    To = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    Country = models.CharField(max_length=100, null=True)
    ticketPrice = models.CharField(max_length=100, null=True)
    flightName = models.CharField(max_length=100, null=True)
    time = models.DateTimeField(null=True)
    flightPic = models.ImageField(upload_to=os.path.join('static', 'flightPic'), default='No profile')
    status = models.CharField(max_length=50,default='Available')

    def __str__(self):
        return self.flightName
    
    class Meta:
        db_table = 'addFlightsModel'

class addHotelsModel(models.Model):
    hotelId = models.AutoField(primary_key=True)
    hotelName = models.CharField(max_length=100, null=True)
    Location = models.CharField(max_length=100, null=True)
    Country = models.CharField(max_length=100, null=True)
    hotelPic = models.ImageField(upload_to=os.path.join('static', 'hotelPic'), default='No profile')
    price = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=100, null=True)
    Address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.hotelName
    
    class Meta:
        db_table = 'addHotelsModel'

class carModel(models.Model):
    carId = models.AutoField(primary_key=True)
    carCompany = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=50, null=True)
    Country = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=50, null=True)
    Location = models.CharField(max_length=100, null=True)
    carPic = models.ImageField(upload_to=os.path.join('static', 'carPic'), default='No profile')
    bookingStatus = models.CharField(max_length=50, default='Available')

    def __str__(self):
        return self.carCompany
    
    class Meta:
        db_table = 'carModel'

class HospitalModel(models.Model):
    hospitalId = models.AutoField(primary_key=True)
    hospitalName = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=50, null=True)
    Country = models.CharField(max_length=100, null=True)
    Location = models.CharField(max_length=100, null=True)
    hospitalPic = models.ImageField(upload_to=os.path.join('static', 'hospitalPic'), default='No profile')
    h_emergency_mail = models.EmailField(null=True)
    open = models.TimeField(null=True)
    closes = models.TimeField(null=True)
    Address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.hospitalName
    
    class Meta:
        db_table = 'HospitalModel'


class PaymentModel(models.Model):
    paymentID = models.AutoField(primary_key=True)
    payment_for = models.CharField(max_length=50, null=True)
    Booking_ID = models.IntegerField(null=True)
    paymenter_name = models.CharField(max_length=50, null=True)
    paymenter_mail = models.EmailField(null=True)
    card_no = models.CharField(max_length=100, null=True)
    paid_amount = models.IntegerField(null=True)
    timeStamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.paymenter_name
    
    class Meta:
        db_table = 'PaymentModel'

class emergencyMail(models.Model):
    emergencyMailID = models.AutoField(primary_key=True)
    hospitalMail = models.EmailField(null=True)
    userEmail = models.EmailField(null=True)
    timeStamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.userEmail
    
    class Meta:
        db_table = 'emergencyMail'
