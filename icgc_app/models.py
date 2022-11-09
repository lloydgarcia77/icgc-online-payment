from django.db import models
from django.db import models
from django.db.models import Q
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.base import Model
from django.utils.text import slugify
from django.urls import reverse
from django.utils.timezone import make_aware, now  
from datetime import datetime  
import uuid, os
# Create your models here.

from icgc_app.lsgfunctools.file_validator import file_validator_pdf, file_validator_image


class UserManager(BaseUserManager):
    """Manger for user profiles"""

    def create_user(self, email, f_name, m_name, l_name, gender, dob, age, contact_no, address, password=None):
        """Create a new user profile"""

        if not email:
            raise ValueError('User must have email address')

        email = self.normalize_email(email)
        user = self.model(email=email, f_name=f_name, m_name=m_name, l_name=l_name, gender=gender, dob=dob, age=age, contact_no=contact_no, address=address,  password=password)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_staffuser(self, email, f_name, m_name, l_name, gender, dob, age, contact_no, address, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email=email, f_name=f_name, m_name=m_name, l_name=l_name, gender=gender, dob=dob, age=age, contact_no=contact_no, address=address,  password=password)
        user.staff = True
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, f_name, m_name, l_name, gender, dob, age, contact_no, address, password):
        """Create and save a new superuser with the given details"""
        user = self.create_user(email=email, f_name=f_name, m_name=m_name, l_name=l_name, gender=gender, dob=dob, age=age, contact_no=contact_no, address=address,  password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Customized model for user in django"""
    MALE = 'male'
    FEMALE = 'female'

    GENDER_LIST = (
        (MALE,'MALE'),
        (FEMALE,'FEMALE'),
    )
 
    email = models.EmailField(max_length=50, unique=True)   
    image = models.ImageField(upload_to="images/", blank=True, validators=[file_validator_image])
    s_name =  models.CharField(max_length=50, blank=True, null=True)
    f_name = models.CharField(max_length=50, verbose_name="First Name")
    m_name = models.CharField(max_length=50, verbose_name="Middle Name")
    l_name = models.CharField(max_length=50, verbose_name="Last Name")
    gender =  models.CharField(max_length=10, choices=GENDER_LIST, default=MALE)
    dob = models.DateField()
    age = models.IntegerField()
    contact_no =  models.CharField(max_length=15,  unique=True)
    address  = models.TextField()
    date_added = models.DateTimeField(auto_now=True) 
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['f_name','m_name','l_name','age','gender', 'dob','contact_no', 'address',] # Email & Password are required by default.

    def get_encrpted_id(self):
        return settings.SIGNER.sign(self.id)

    
    def get_full_name(self):
        return f'{self.l_name}, {self.f_name} {self.m_name}'
    
    
    def get_short_name(self):
        return self.f_name
    

    def get_encrpted_id(self):
        return settings.SIGNER.sign(self.id)

    
    def __str__(self):
        return self.email
      
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    
    def image_name(self):     
        return os.path.basename(self.image.name) if self.image else '-'  
    
        
    def image_extension(self): 
        if self.image:
            name, extension = os.path.splitext(self.image.name)
            return extension
        else:
            return '-'

    
    def delete(self,*args,**kwargs):
        if self.image:
            if os.path.isfile(self.image.path) and os.path.exists(self.image.path):
                os.remove(self.image.path)  
        super(User, self).delete(*args,**kwargs)
   

class Game(models.Model): 
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    slug = models.SlugField(max_length=200, blank=True, null=True, unique=True)
    name = models.CharField(max_length=255)
    img_thumbnail = models.ImageField(upload_to="game/thumbnail/", blank=True, validators=[file_validator_image])
    img_wallpaper = models.ImageField(upload_to="game/wallpaper/", blank=True, validators=[file_validator_image])
    title = models.CharField(max_length=255)
    website = models.URLField(max_length=255, null=True, blank=True)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # def image_name(self):     
    #     return os.path.basename(self.image.name) if self.image else '-'  
    
        
    # def image_extension(self): 
    #     if self.image:
    #         name, extension = os.path.splitext(self.image.name)
    #         return extension
    #     else:
    #         return '-'

    
    def delete(self,*args,**kwargs):
        if self.img_thumbnail:
            if os.path.isfile(self.img_thumbnail.path) and os.path.exists(self.img_thumbnail.path):
                os.remove(self.img_thumbnail.path)  
        if self.img_wallpaper:
            if os.path.isfile(self.img_wallpaper.path) and os.path.exists(self.img_wallpaper.path):
                os.remove(self.img_wallpaper.path)  
        super(Game, self).delete(*args,**kwargs)

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

      
    def get_absolute_url_view(self):
        return reverse('icgc_app:game_items', args=[self.slug,])

class Amount(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    game = models.ForeignKey(Game, related_name='fk_amount_game', on_delete=models.CASCADE)
    pin = models.CharField(max_length=50, unique=True)
    sn = models.CharField(max_length=50, unique=True)
    amount = models.IntegerField()
    points_to_earn = models.IntegerField(default=0)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.game.title} ({self.amount}) - {self.points_to_earn}pte'
    
    def get_absolute_url_details(self):
        return reverse('icgc_app:game_get_amount_details', args=[self.game.slug, self.id])

class PaymentMethod(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    img_thumbnail = models.ImageField(upload_to="game/payment_method/", blank=True, validators=[file_validator_image])
    name = models.CharField(max_length=100, unique=True)
    channel_code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def delete(self,*args,**kwargs):
        if self.img_thumbnail:
            if os.path.isfile(self.img_thumbnail.path) and os.path.exists(self.img_thumbnail.path):
                os.remove(self.img_thumbnail.path)  
       
        super(PaymentMethod, self).delete(*args,**kwargs)

    # def get_absolute_url_details(self):
    #     return reverse('icgc_app:game_get_payment_method_details', args=[self.id])


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    reference_id = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, related_name='fk_transactions_user', on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.ForeignKey(Amount, related_name='fk_transactions_amount', on_delete=models.SET_NULL, blank=True, null=True)
    game = models.ForeignKey(Game, related_name='fk_transactions_game', on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.ForeignKey(PaymentMethod, related_name='fk_transactions_payment_method', on_delete=models.SET_NULL , blank=True, null=True)
    email = models.EmailField(blank=True, null=True, max_length=50)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    charge_id = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return str(self.transaction_id)
    
    def get_absolute_url_check_status(self):
        return reverse('icgc_app:transaction_status', args=[self.transaction_id])
    
    def get_absolute_url_delete(self):
        return reverse('icgc_app:delete_transaction', args=[self.transaction_id])

    def get_absolute_url_void(self):
        return reverse('icgc_app:void_transaction', args=[self.transaction_id])

    def get_absolute_url_refund(self):
        return reverse('icgc_app:refund_transaction', args=[self.transaction_id])

    def get_absolute_url_list_refund(self):
        return reverse('icgc_app:list_refund_transaction', args=[self.transaction_id])
    
    def get_absolute_url_send_po_to_email(self):
        return reverse('icgc_app:transaction_po_send_mail', args=[self.transaction_id])
