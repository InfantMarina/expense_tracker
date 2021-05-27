from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user

class MPRO_User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, default='admin@admin.com')
    name = models.CharField(max_length=254, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

class Account(models.Model):
    account_name = models.CharField(max_length=35,null=False,blank=False)
    account_holder = models.ForeignKey(MPRO_User, on_delete=models.CASCADE, related_name='account_mprouser')
    created_date = models.DateTimeField(auto_now_add=True)
    balance = models.IntegerField()

class Icon(models.Model):
    icon_name = models.CharField(max_length=20,null=False,blank=False)
    path = models.CharField(max_length=100,null=False,blank=False)

class CategoryMaster(models.Model):
    category_name = models.CharField(max_length=20,null=False,blank=False)
    category_type = models.CharField(max_length=20,null=False,blank=False)
    is_child = models.BooleanField()
    parent_category = models.IntegerField()
    # icon_name = models.ForeignKey(Icon, on_delete=models.CASCADE, related_name='account_icon')
    color = models.CharField(max_length=20,null=False,blank=False)
    categorized_by = models.ForeignKey(MPRO_User, on_delete=models.CASCADE, related_name='category_mprouser')

class Transaction(models.Model):
    transaction_type = models.CharField(max_length=15,null=False,blank=False)
    account_id = models.ForeignKey(Account,on_delete=models.CASCADE, related_name='account_account')
    amount = models.IntegerField()
    description = models.CharField(max_length=20,null=False,blank=False)
    category = models.ForeignKey(CategoryMaster,on_delete=models.CASCADE, related_name='account_categorymaster')
    payee = models.CharField(max_length=20,null=False,blank=False)
    transaction_date = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(MPRO_User, on_delete=models.CASCADE, related_name='transaction_mprouser')

class TransactionHistory(models.Model):
    transaction_id = models.ForeignKey(Transaction,on_delete=models.CASCADE, related_name='account_transaction')
    column_name = models.CharField(max_length=20,null=False,blank=False)
    previous_value = models.IntegerField()
    current_value = models.IntegerField()
    modified_date = models.DateTimeField()
    modified_by = models.ForeignKey(MPRO_User, on_delete=models.CASCADE, related_name='transactionhistory_mprouser')

class LoginHistory(models.Model):
    login_user = models.ForeignKey(MPRO_User, on_delete=models.CASCADE, related_name='loginhistory_mprouser')
    date = models.DateTimeField(auto_now_add=True)