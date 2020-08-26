from django.contrib import admin
from .models import User
import string
from django.urls import reverse
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import csv
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
    parameter_name = 'date_joined'

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
            hour = (today - datetime.timedelta(hours=6))
            
            return queryset.filter(date_joined__gte=hour)
        elif self.value() == '7':
            h1 = (today - datetime.timedelta(hours=7))
            
            h2 = (today - datetime.timedelta(hours=13))
            
            return queryset.filter(date_joined__gte=h2, date_joined__lte=h1)
        elif self.value() == '14':
            h1 = (today - datetime.timedelta(hours=14))
            

            h2 = (today - datetime.timedelta(hours=20))
            
            return queryset.filter(date_joined__gte=h2, date_joined__lte=h1)
        elif self.value() == '21':
            h1 = (today - datetime.timedelta(hours=21))

            h2 = (today - datetime.timedelta(hours=27))
            
            return queryset.filter(date_joined__gte=h2, date_joined__lte=h1)
        




def change_user_status(obj):
    """"
        This is a function that takes a user object as an argument and passes the ID to the view and changes the current status of the user.
    """
    url = reverse('main:deactivate', args=[obj.id])
    return mark_safe(f"<button style='border:1px solid; border-radius:3px'><a href='{url}''>Change Status</a></button>")



#converting the list of users
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'






@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    change_list_template = 'admin/change_list.html'
    list_display = ['first_name', 'last_name', 'username', 'email', 'phone', 'is_active', change_user_status ]
    list_filter = ['date_joined','is_active', TimeFilter, AlphabetFilter]
    date_hierarchy = 'date_joined'
    actions = [export_to_csv]