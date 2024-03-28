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


        