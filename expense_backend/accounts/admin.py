from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import AccountModel
from .models import UserInfoModel
# Here we register our user model and handle Django Admin for accounts
class AccountModelAdmin(BaseUserAdmin):
    model = AccountModel
    list_display = ['email', 'user_firstname', 'user_lastname',
                    'user_permission', 'is_active', 'is_staff']

    # Categorising our data 
    # Looks like a bit of bloat but it follows
    # a format that is similar to JSON files.

    # These are fields to be used in displaying the User Model.
    # They override the definitions on base UserAdmin
    # that reference specific fields on auth.User.
    fieldsets = (
        (None, {'fields' : ('email', 'password')}),
        ('Personal info', {'fields' : ('user_firstname', 'user_lastname')}),
        ('Permissions', {'fields' : ('user_permission', 'is_active',
                                    'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields': ('email', 'user_firstname', 'user_lastname',
                        'password1', 'password2'),
            }
         ),
    )

    search_fields = ('email', 'user_firstname', 'user_lastname')
    ordering = ('email',)
    filter_horizontal=()

admin.site.register(AccountModel, AccountModelAdmin)
admin.site.register(UserInfoModel)
