from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.db import models



# This class extends the BaseUserManager 
# interface to create regular and super users.
class AccountManager(BaseUserManager):

    # Creating a user with given email, firstname, lastname
    # and password.
    def create_user(self, email, user_firstname, user_lastname,
                    password=None, **extra_fields):
        
        # Handling empty inputs.
        if not email:
            raise ValueError('The Email field must be set')
        if not user_firstname:
            raise ValueError('The Firstname field must be set')
        if not user_lastname:
            raise ValueError('The Lastname field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        
        # Setting fields with data passed into the function
        # and returning the user.
        email = self.normalize_email(email)
        user = self.model(email=email, user_firstname=user_firstname,
                          user_lastname=user_lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    # Creating a super user that can access the DB directly.
    # This should ideally be just the Admin.
    # --- NOTES ---
    # Sepehr - I need to do some more testing for this and see 
    # where it is exactly needed.
    def create_superuser(self, email, user_firstname, user_lastname,
                         password=None, **extra_fields):

        # Setting default tags for a Super User.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Checking the tags.
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # Calling the create user function to 
        # create our superuser with the given fields
        # and returning the result - which is our actual superuser.
        return self.create_user(email, user_firstname,
                                user_lastname, password, **extra_fields)
        


# This class sets up our User Model
# using AbstractBaseUSer and PermissionsMixin interfaces.
# Current structure's defaults:
#   - Permission level is EMPLOYEE
#   - User is not staff
#   - User is active

# --- NOTES ---
# Sepehr - I need to configure the Meta further later on
# based on our needs, but the basics for now should do.

class AccountModel(AbstractBaseUser, PermissionsMixin):
    
    # The Meta class just takes care of some
    # "aesthetics" and ordering
    # This includes ordering fields and giving verbose names.
    class Meta:
        ordering = ['user_lastname', 'user_firstname']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        db_table = 'user_account'
        unique_together = (('user_firstname', 'email'),)


    # Setting up our permission levels:
    PERMISSION_CHOICES = (
        ('EMPLOYEE', 'Employee'),
        ('LINEMANAGER', 'Line Manager'),
        ('FINANCE', 'Finance'),
        ('ADMIN', 'Admin'),
    )

    # Setting up our table structure:
    user_id = models.AutoField(primary_key=True)
    user_firstname = models.CharField(max_length=50)
    user_lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_permission = models.CharField(max_length=20,
                                       choices=PERMISSION_CHOICES,
                                       default='EMPLOYEE')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_firstname', 'user_lastname']

    objects = AccountManager()

    def __str__(self):
        return self.email

        
#This model is to contain the information for the employee claim data
class EmployeeFormModel(models.Model):
    # Setting up claim status and claim types:
    CLAIM_STATUS = (
        ('ACCEPTED', 'accepted'),
        ('REJECTED', 'rejected'),
        ('PENDING', 'pending'),

    )

    CLAIM_TYPE = (
        ('TRAVEL', 'travel'),
        ('MEAL', 'meal'),
        ('NIGHTSTAY', 'night stay'),
        ('GIFT', 'gift'),

    )


    claimID = models.AutoField(primary_key=True)

    # Foreign Key linking so that userID in this table 
    # is related with AccountModel.
    user_id = models.ForeignKey(
            AccountModel,
            on_delete=models.CASCADE, # Delete from both tables if user is deleted.
            related_name='claims', # This lets us access a user's claim with user.claims
            null=True,
            blank=True,
            default='',
    )


    lineManagerID = models.CharField(max_length=100, null=True, blank=True)
    amount =  models.FloatField(default=0.0)
    currency = models.CharField(max_length=100)
    typeClaim = models.CharField(max_length=20,choices=CLAIM_TYPE,
                                       default='meal')
    description = models.CharField(max_length=100)
    receipt = models.ImageField(null=True, blank=True, upload_to="receipts/")
    acknowledgement = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=CLAIM_STATUS,
                                       default='PENDING')
    
    def get_receipt_url(self):
        if self.receipt and hasattr(self.reciept, 'url'):
            return self.receipt.url
        else:
            return "/static/images/user.jpg"
    
#This model is to contain the information for each employee
class UserInfoModel(models.Model):
    userID = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    account_number = models.CharField(max_length=8)
    sort_code = models.CharField(max_length=8)
    tax_code = models.CharField(max_length=100)
    manager_id = models.IntegerField(null=True, blank=True)  # Assuming some users may not have managers
