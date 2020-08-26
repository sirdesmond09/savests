from django.contrib import admin
from .models import User
import string
from django.urls import reverse
from django.utils.safestring import mark_safe
import datetime

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


class TimeFilter(admin.SimpleListFilter):
    title = 'time'
    parameter_name = 'time_joined'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('0', ('Less than 7 hrs')),
            ('7', ('7-13 hrs')),
            ('14', ('14-20 hrs')),
            ('21', ('21-24 hrs')),
            
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        today = datetime.datetime.now()
        if self.value() == '0':
            hour = (today - datetime.timedelta(hours=6)).hour
            minute = (today - datetime.timedelta(hours=6)).minute
            time = f"{hour}:{minute}"
            return queryset.filter(time_joined__gte=time)
        elif self.value() == '7':
            h1 = (today - datetime.timedelta(hours=7)).hour
            m1 = (today - datetime.timedelta(hours=7)).minute
            t1 = f"{hour}:{minute}"

            h2 = (today - datetime.timedelta(hours=13)).hour
            m2 = (today - datetime.timedelta(hours=13)).minute
            t2 = f"{hour}:{minute}"
            return queryset.filter(time_joined__gte=t2, time_joined__lte=t1)
        elif self.value() == '14':
            h1 = (today - datetime.timedelta(hours=14)).hour
            m1 = (today - datetime.timedelta(hours=14)).minute
            t1 = f"{hour}:{minute}"

            h2 = (today - datetime.timedelta(hours=20)).hour
            m2 = (today - datetime.timedelta(hours=20)).minute
            t2 = f"{hour}:{minute}"
            return queryset.filter(time_joined__gte=t2, time_joined__lte=t1)
        elif self.value() == '21':
            h1 = (today - datetime.timedelta(hours=21)).hour
            m1 = (today - datetime.timedelta(hours=21)).minute
            t1 = f"{hour}:{minute}"

            h2 = (today - datetime.timedelta(hours=27)).hour
            m2 = (today - datetime.timedelta(hours=27)).minute
            t2 = f"{hour}:{minute}"
            return queryset.filter(time_joined__gte=t2, time_joined__lte=t1)
        




def change_user_status(obj):
    """"
        This is a function that takes a user object as an argument and passes the ID to the view and changes the current status of the user.
    """
    url = reverse('main:deactivate', args=[obj.id])
    return mark_safe(f"<button style='border:1px solid; border-radius:3px'><a href='{url}''>Change Status</a></button>")




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list.html'
    list_display = ['first_name', 'last_name', 'username', 'email', 'phone', 'is_active', change_user_status ]
    list_filter = ['date_joined','is_active', TimeFilter, AlphabetFilter]
    date_hierarchy = 'date_joined'
