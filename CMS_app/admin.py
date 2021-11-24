from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from .models import CAM_demand, CustomUser, client, commercial_shop, flat, invoice, plot
from .models import recovery_call_followup, recovery_schedule_call, recovery_task, rental, society, block
from .models import floor, society_expense, villa, electricity_bill, collection_Income, water_bill
from .models import collection_CAM_received, collection_DG, collection_water, collection_rent
from .models import collection_electricity, discount_society, discount_user, report, unit
from .forms import UserSignUpForm
# Register your models here.

# class CustomUserAdmin(UserAdmin):
#    add_form = UserSignUpForm
#    # form = CustomUserChangeForm

#    model = CustomUser
#    list_display = ['username', 'email', 'is_superuser', 'is_staff']
admin.site.register(
    [CAM_demand, client, commercial_shop, flat, invoice, plot, recovery_call_followup, 
    recovery_schedule_call, recovery_task, rental, society, block, floor, society_expense,
    villa, electricity_bill, water_bill, collection_Income, collection_CAM_received,
    collection_DG, collection_water, collection_rent, collection_electricity, discount_society, 
    discount_user, report, unit])

@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    actions_on_top = True    
    list_display = ['username', 'email', 'is_superuser', 'is_staff', 'is_active']
    list_filter = []
