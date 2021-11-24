from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from datetime import date
from .validators import only_digit
# Create your models here.
PROPERTY_TYPE = (
      ('Flat','Flat'),
      ('Villa','Villa'),
      ('Plot','Plot'),
      ('Shop','Shop')
   )

OWNERSHIP = (
   ('Rented','Rented'),
   ('Owned','Owned')
)

OCCUPANCY = (
   ('Occupied','Occupied'),
   ('Vacant','Vacant')
)
class CustomUser(AbstractUser):
   contact = models.CharField(max_length=10, validators=[only_digit])
   
   def __str__(self):
      return self.username

   def full_name(self):
      return self.first_name+" "+self.last_name

class client(models.Model):
   CLIENT_TYPE = (
      ('Client/Resident','Client/Resident'),
      ('Role Based User','Role Based User'),
   )   
   user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True)
   first_name = models.CharField(max_length=150)
   last_name = models.CharField(max_length=150)
   mobile_number = models.CharField(max_length=10, validators=[only_digit])
   email_address = models.EmailField(max_length=50)
   permanent_address = models.CharField(max_length=512)
   current_address = models.CharField(max_length=512)
   aadhar_number = models.CharField(max_length=12)
   PAN_number = models.CharField(max_length=10)
   user_type = MultiSelectField(choices=CLIENT_TYPE)
   registry_date = models.DateField()
   booking_date = models.DateField()
   occupancy_date = models.DateField()

   def __str__(self):
      return self.user.username

class society(models.Model):
   society_title = models.CharField(max_length=256)
   society_brand = models.CharField(max_length=256)
   society_description = models.TextField()
   society_image = models.ImageField(upload_to='society_images')
   site_plan = models.FileField(upload_to='society_site_plan')
   lease_out_plan = models.FileField(upload_to='society_lease_out_plan')

   def __str__(self):
      return self.society_title

class block(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   block = models.CharField(max_length=100)

   def __str__(self):
      return self.block

class floor(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   blocks = models.ForeignKey(block, on_delete=models.CASCADE)
   floor = models.PositiveIntegerField(default=0)

   def __str__(self):
      return self.society.society_title+"floor"

class flat(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   flat_number = models.PositiveIntegerField()
   bedroom = models.PositiveIntegerField()
   hall = models.PositiveIntegerField()
   kitchen = models.PositiveIntegerField()
   balcony = models.PositiveIntegerField()
   Area = models.CharField(max_length=20)
   ownership = models.CharField(choices=OWNERSHIP, max_length=150, default='Rented')
   occupancy = models.CharField(choices=OCCUPANCY, max_length=150, default='Occupied')

   def __str__(self):
      return self.society.society_title+' Flat-'+str(self.flat_number)

class villa(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   villa_number = models.PositiveIntegerField()
   length = models.PositiveIntegerField()
   width = models.PositiveIntegerField()
   area = models.PositiveIntegerField()
   ownership = models.CharField(max_length = 150, choices=OWNERSHIP, default='Rented')
   occupancy = models.CharField(max_length = 150, choices=OCCUPANCY, default='Occupied')

   def __str__(self):
      return self.society.society_title+" Villa-"+str(self.villa_number)

class plot(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   plot_number = models.PositiveIntegerField()
   length = models.PositiveIntegerField()
   width = models.PositiveIntegerField()
   area = models.PositiveIntegerField()
   ownership = models.CharField(max_length = 150, choices=OWNERSHIP, default='Rented')
   occupancy = models.CharField(max_length = 150, choices=OCCUPANCY, default='Occupied')

   def __str__(self):
      return self.society.society_title+" Plot-"+str(self.plot_number)

class commercial_shop(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE, null=True)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE, null=True)
   shop_number = models.PositiveIntegerField()
   length = models.PositiveIntegerField()
   width = models.PositiveIntegerField()
   area = models.PositiveIntegerField()
   ownership = models.CharField(max_length = 150, choices=OWNERSHIP, default='Rented')
   occupancy = models.CharField(max_length = 150, choices=OCCUPANCY, default='Occupied')

   def __str__(self):
      return self.society.society_title+" Commercial Shop-"+str(self.shop_number)

class assigned_property(models.Model):
   client_ID = models.IntegerField()
   date = models.DateField()
   first_name = models.CharField(max_length=100)
   last_name = models.CharField(max_length=100)
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   type_of_property = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   property_number = models.IntegerField()
   rent = models.BooleanField(default=False)
   CAM = models.CharField(max_length=10)

class society_expense(models.Model):   
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   expense_by = models.CharField(max_length=150)
   reason = models.TextField()
   Amount = models.PositiveIntegerField()
   date = models.DateField()
   invoice = models.FileField(upload_to='society-expense/invoice')

class rental(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   property_number = models.PositiveIntegerField()
   rent = models.PositiveIntegerField()
   date = models.DateField()

class CAM_demand(models.Model):
   date = models.DateField()
   reference_number = models.PositiveIntegerField()
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   property_number = models.PositiveIntegerField()
   client_name = models.CharField(max_length=150)
   demand = models.CharField(max_length=10)
   CAM_charges = models.CharField(max_length=10)

   def __str__(self):
      return self.reference_number

class CAM_calculation(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   property_number = models.PositiveIntegerField()
   client_name = models.CharField(max_length=150)
   CAM = models.DecimalField(max_digits=10, decimal_places=2)

PAYMENTMODE = (
   ('Cash','Cash'),
   ('UPI', 'UPI'),
   ('Net Banking', 'Net Banking')
)
class invoice(models.Model):
   date = models.DateField()
   name = models.CharField(max_length=100)
   amount = models.DecimalField(max_digits=12, decimal_places=2)
   mode_of_payment = models.CharField(choices=PAYMENTMODE, max_length=100)
   property_type = models.CharField(max_length=100, choices=PROPERTY_TYPE)
   property_number = models.PositiveIntegerField()
   drawn_on = models.DateField()
   purpose = models.CharField(max_length=256)
   upload = models.FileField(upload_to='Recovery_management/invoice')

   def __str__(self):
      return self.name

class recovery_schedule_call(models.Model):
   client_name = models.CharField(max_length=100)
   date = models.DateField()
   time = models.TimeField()
   call_by = models.CharField(max_length=100)

class recovery_call_followup(models.Model):
   client_name = models.CharField(max_length=100)
   date = models.DateField()
   time = models.TimeField()
   follow_up = models.TextField()

class recovery_task(models.Model):
   task_name = models.CharField(max_length=100)
   date = models.DateField()
   time = models.TimeField()
   task_detail = models.TextField()
   assign_to = models.CharField(max_length=100)

   def __str__(self):
      return self.task_name

class electricity_bill(models.Model):
   society = models.ForeignKey(society , on_delete=models.CASCADE)
   block = models.ForeignKey(block , on_delete=models.CASCADE)
   floor = models.ForeignKey(floor , on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   property_number = models.PositiveIntegerField()
   client_name = models.CharField(max_length=100)
   consumption_unit = models.DecimalField(max_digits=7 , decimal_places=2)
   per_unit_charge = models.DecimalField(max_digits=7 , decimal_places=2)

   def __str__(self):
      return self.client_name

class water_bill(models.Model):
   
   society = models.ForeignKey(society , on_delete=models.CASCADE)
   block = models.ForeignKey(block , on_delete=models.CASCADE)
   floor = models.ForeignKey(floor , on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   property_number = models.PositiveIntegerField()
   client_name = models.CharField(max_length=100)
   consumption_unit = models.DecimalField(max_digits=7 , decimal_places=2)
   per_unit_charge = models.DecimalField(max_digits=7 , decimal_places=2)

   def __str__(self):
      return self.client_name
UNITCHOICE=(
   ('Water','Water'),
   ('Electricity', 'Electricity'),
)
class unit(models.Model):   
   society = models.ForeignKey(society , on_delete=models.CASCADE)
   unit_for = models.CharField(max_length=100, choices=UNITCHOICE)
   type_of_unit = models.CharField(max_length=100)

class discount_society(models.Model):
   society = models.ForeignKey(society , on_delete=models.CASCADE)
   block = models.ForeignKey(block , on_delete=models.CASCADE)
   period = models.CharField(max_length=3)
   dis_per = models.DecimalField(max_digits=4 , decimal_places=2)

class discount_user(models.Model):
   society = models.ForeignKey(society , on_delete=models.CASCADE)
   block = models.ForeignKey(block , on_delete=models.CASCADE)
   floor = models.ForeignKey(floor , on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   property_number = models.CharField(max_length=50)
   cam = models.CharField(max_length=100)
   dis_per = models.DecimalField(max_digits=4 , decimal_places=2)
   dis_cam = models.DecimalField(max_digits=7 , decimal_places=2)
   valid_period = models.CharField(max_length=3)

class report(models.Model):   
   From = models.DateField()
   To = models.DateField()
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
      
class collection_CAM_received(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   client_name = models.CharField(max_length=100)
   CAM_demand = models.CharField(max_length=100)
   CAM_received = models.CharField(max_length=100)
   date = models.DateField()

class collection_rent(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   client_name = models.CharField(max_length=100)
   rent_generated = models.CharField(max_length=100)
   rent_received = models.CharField(max_length=100)
   date = models.DateField()   

class collection_electricity(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   client_name = models.CharField(max_length=100)
   electricity_generated = models.CharField(max_length=100)
   electricity_received = models.CharField(max_length=100)
   date = models.DateField() 

class collection_water(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   client_name = models.CharField(max_length=100)
   water_bill_generated = models.CharField(max_length=100)
   water_bill_received = models.CharField(max_length=100)
   date = models.DateField()   

class collection_DG(models.Model):
   society = models.ForeignKey(society, on_delete=models.CASCADE)
   property_type = models.CharField(choices=PROPERTY_TYPE, max_length=100)
   floor = models.ForeignKey(floor, on_delete=models.CASCADE)
   block = models.ForeignKey(block, on_delete=models.CASCADE)
   client_name = models.CharField(max_length=100)
   bill_generated = models.CharField(max_length=100)
   bill_received = models.CharField(max_length=100)
   DG_used = models.CharField(max_length=100)
   date = models.DateField() 

class collection_Income(models.Model):
   YEAR_CHOICES = [(r,r) for r in range(1984, date.today().year+1)]
   year = models.IntegerField(('year'), choices=YEAR_CHOICES, default=datetime.now().year)
   amount = models.IntegerField()
   ROI = models.CharField(max_length=100)
   month = models.IntegerField()
   income_from_fund = models.IntegerField()