from django.contrib import admin
from .models import User
import string
from django.urls import reverse
from django.utils.safestring import mark_safe


# Register your models here.

class AlphabetFilter(admin.SimpleListFilter):
    title = 'alphabet'
    parameter_name = 'alphabet'

    def lookups(self, request, model_admin):
        abc = list(string.ascii_lowercase)
        return (([c.upper(), c.upper()]) for c in abc)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(first_name__startswith=self.value())

def change_user_status(obj):
    """"
        This is a function that takes a user object as an argument and passes the ID to the view and changes the current status of the user.
    """
    url = reverse('main:deactivate', args=[obj.id])
    return mark_safe(f"<button style='border:1px solid; border-radius:3px'><a href='{url}''>Change Status</a></button>")



def send_mail(obj):
    """"
        This is a function that takes a user object as an argument and passes the ID to the view and changes the current status of the user.
    """
    url = reverse('main:send_mail')
    return mark_safe(f"<button style='border:1px solid; border-radius:3px'><a href='{url}''>Send email</a></button>")




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list.html'
    list_display = ['first_name', 'last_name', 'username', 'email', 'phone', 'is_active', change_user_status ]
    list_filter = ['date_joined', 'time_joined', 'is_active', AlphabetFilter]
    date_hierarchy = 'date_joined'
    # time_hierarchy =  'time_joined'