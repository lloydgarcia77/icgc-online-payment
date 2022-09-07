from django.contrib import admin 
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from icgc_app.forms import UserAdminCreationForms, UserAdminChangeForm
from icgc_app import models

admin.site.site_header = 'I Care Game Credits Super Administrator'
admin.site.index_title = 'Super Administrator Page'
admin.site.site_title = 'Super Administrator Panel'
# Register your models here.

User = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # the forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForms

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'is_staff','is_active', 'is_superuser']
    list_filter = ['is_staff']

    fieldsets = (
        ("Account", {
            'fields': 
                (
                    'email', 
                    'password',
                )
        }), 
        ('Personal Info', {'fields': (
            'image',
            'f_name',
            'm_name',
            'l_name',
            'gender',
            'dob',
            'age',
            'address',
            'contact_no', 
        )}),
        ('Permission', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser'
                )
            }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    
    add_fieldsets = (
       
         ('Personal Info', {'fields': (
            'image',
            'f_name',
            'm_name',
            'l_name',
            'gender',
            'dob',
            'age',
            'address',
            'contact_no', 
        )}),
        ('Permission', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser'
                )
        }),
        (
            "Account", {
                'classes': ('wide', ),
                'fields': ('email', 'password', 'password_2')
            }
        ),
    )

    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

 
class GameAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Game._meta.get_fields() if 'fk' not in field.name]
    list_editable = ("name","title","description",)
    list_per_page = 10
    search_fields = ("name","title",)
    list_filter = ("date_created",)
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'date_created'
    ordering = ["date_created",] 

admin.site.register(models.Game, GameAdmin) 


class AmountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Amount._meta.get_fields() if 'fk' not in field.name]
    list_editable = ("pin","sn","amount","description",)
    list_per_page = 10
    search_fields = ("pin","sn","amount","description",)  
    date_hierarchy = 'date_created'
    ordering = ['date_created',]

admin.site.register(models.Amount, AmountAdmin) 