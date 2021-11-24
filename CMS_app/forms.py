from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import CAM_calculation, CAM_demand, CustomUser, assigned_property, client, collection_CAM_received, collection_DG, collection_Income, collection_electricity, discount_society, discount_user, electricity_bill, unit, water_bill
from .models import commercial_shop, flat, invoice, plot, recovery_call_followup
from .models import recovery_schedule_call, recovery_task, rental, report, society, block, floor
from .models import society_expense, villa, collection_rent, collection_water 

class UserSignUpForm(UserCreationForm):
   class Meta:
      model = CustomUser
      fields = ['first_name', 'last_name','username', 'email', 'contact', 'password1', 'password2']
      

class ClientUserForm(UserCreationForm):
   class Meta():
      model = CustomUser
      fields = ['username', 'email', 'contact', 'password1', 'password2']

class ClientForm(forms.ModelForm):
   class Meta():
      model = client
      fields = [
         'first_name', 'last_name', 'mobile_number', 'email_address', 'permanent_address', 
         'current_address', 'aadhar_number', 'PAN_number', 'user_type', 
         'registry_date', 'booking_date', 'occupancy_date'
         ]

class SocietyForm(forms.ModelForm):
   class Meta():
      model = society
      fields = '__all__'
      widgets={
         'society_description':forms.Textarea(attrs={'rows':4, 'cols':15})
      }
class BlockForm(forms.ModelForm):
   class Meta():
      model = block
      fields = '__all__'

class FloorForm(forms.ModelForm):
   class Meta():
      model = floor
      fields = '__all__'

class FlatForm(forms.ModelForm):
   class Meta():
      model = flat
      fields = '__all__'
      widgets = {
         'ownership':forms.RadioSelect(),
         'occupancy':forms.RadioSelect()
      }

class VillaForm(forms.ModelForm):
   class Meta():
      model = villa
      fields = '__all__'
      widgets = {
         'ownership':forms.RadioSelect(),
         'occupancy':forms.RadioSelect()
      }
class PlotForm(forms.ModelForm):
   class Meta():
      model = plot
      fields = '__all__'
      widgets = {
         'ownership':forms.RadioSelect(),
         'occupancy':forms.RadioSelect()
      }
class ShopForm(forms.ModelForm):
   class Meta():
      model = commercial_shop
      fields = '__all__'
      widgets = {
         'ownership':forms.RadioSelect(),
         'occupancy':forms.RadioSelect()
      }

class AssignedPropertyForm(forms.ModelForm):
   class Meta():
      model = assigned_property
      fields = '__all__'

class SocietyExpenseForm(forms.ModelForm):
   class Meta():
      model = society_expense
      fields = '__all__'
      widgets = {
         'reason':forms.Textarea(attrs={'rows':4, 'cols':15})
      }
class RentalForm(forms.ModelForm):
   class Meta():
      model = rental
      fields = '__all__'

class DemandCreationForm(forms.ModelForm):
   class Meta():
      model = CAM_demand
      fields = '__all__'

class CamCalculationForm(forms.ModelForm):
   class Meta():
      model = CAM_calculation
      fields = '__all__'      
class RecoveryInvoiceForm(forms.ModelForm):
   class Meta():
      model = invoice
      fields = '__all__'
class RecoveryScheduleCallForm(forms.ModelForm):
   
   class Meta():
      model = recovery_schedule_call
      fields = '__all__'
      widgets = {
         'time':forms.TimeInput(format='%I:%M %p'),
      }

class RecoveryCallFollowupForm(forms.ModelForm):
   class Meta():
      model = recovery_call_followup
      fields = '__all__'
      widgets = {
         'follow_up':forms.Textarea(attrs={'rows':4, 'cols':15})
      }
class RecoveryTaskForm(forms.ModelForm):
   class Meta():
      model = recovery_task
      fields = '__all__'
      widgets = {
         'task_detail':forms.Textarea(attrs={'rows':4, 'cols':15})
      }

class ReportForm(forms.ModelForm):
   class Meta():
      model = report
      fields = '__all__'

class ElectricityBillForm(forms.ModelForm):
   class Meta():
      model = electricity_bill
      fields = '__all__'

class WaterBillForm(forms.ModelForm):
   class Meta():
      model = water_bill
      fields = '__all__'

class UnitForm(forms.ModelForm):
   class Meta():
      model = unit
      fields = '__all__'

class DiscountSocietyForm(forms.ModelForm):
   class Meta():
      model = discount_society
      fields = '__all__'

class DiscountUserForm(forms.ModelForm):
   class Meta():
      model = discount_user
      fields = '__all__'

class CollectionCAMReceivedForm(forms.ModelForm):
   class Meta():
      model = collection_CAM_received
      fields = '__all__'

class CollectionRentForm(forms.ModelForm):
   class Meta():
      model = collection_rent
      fields = '__all__'

class CollectionElectricityForm(forms.ModelForm):
   class Meta():
      model = collection_electricity
      fields = '__all__'

class CollectionWaterForm(forms.ModelForm):
   class Meta():
      model = collection_water
      fields = '__all__'

class CollectionDGForm(forms.ModelForm):
   class Meta():
      model = collection_DG
      fields = '__all__'

class CollectionIncomeFromFundForm(forms.ModelForm):
   class Meta():
      model = collection_Income
      fields = '__all__'
