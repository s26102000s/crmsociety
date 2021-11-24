from datetime import datetime
from decimal import Context
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.template.loader import get_template, render_to_string

from .tokens import account_activation_token
from .models import CAM_calculation, CAM_demand, CustomUser, client, collection_Income, commercial_shop, discount_user, electricity_bill, flat, invoice, plot, unit, water_bill
from .models import recovery_call_followup, recovery_schedule_call, recovery_task, rental, society
from .models import block, floor, society_expense, villa, collection_CAM_received,collection_DG, collection_rent
from .models import collection_water, collection_electricity, report
from . import forms
from . import filters
from .decorators import unauthenticated_user

# Create your views here.
"""
==================================================================
 Login/Sign-up Related views
==================================================================
"""

@unauthenticated_user
def SignUpView(request):
   form = forms.UserSignUpForm()
   if request.method == 'POST':
      form = forms.UserSignUpForm(request.POST)
      
      if form.is_valid():
         user = form.save(commit=False)
         user.is_active = False
         user.save()

         current_site = get_current_site(request)
         print("signal started")
         mail_subject = 'Activate your account.'
         
         message = render_to_string('crm/user_account_activation_email.html', {
             'user': user,
             'domain': current_site.domain,
             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
             'token':account_activation_token.make_token(user),
         })
         to_email = form.cleaned_data.get('email')
         email = EmailMessage(
                     mail_subject, message, to=[to_email]
         )
         email.send(fail_silently=False)
         print("mail sent")
         messages.success(request, "Your account has been created successfully!!")
         return redirect(reverse("CMS_app:login"))
   return render(request, 'crm/register.html', {'form':form})

def activate(request, uidb64, token):
   try:
       uid = force_text(urlsafe_base64_decode(uidb64))
       user = CustomUser.objects.get(pk=uid)
   except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
       user = None
   if user is not None and account_activation_token.check_token(user, token):
       user.is_active = True
       user.save()
       login(request, user)
       return redirect(reverse('CMS_app:dashboard'))
     #   return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
   else:
       return HttpResponse('Activation link is invalid!')

@unauthenticated_user
def LoginView(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None:
         login(request, user)
         return redirect(reverse('CMS_app:dashboard'))
      else:
         messages.info(request, 'Username or Password is incorrect!!')
   return render(request, 'crm/login.html')

def LogoutView(request):
   logout(request)
   return HttpResponseRedirect('/')

def forget_pass_view(request):
   return render(request, 'crm/forget_pass.html')

"""
==================================================================
 Dashboard Related views
==================================================================
"""

@login_required(login_url='/')
def dashboard(request):
   total_clients = client.objects.all().count()
   total_societies = society.objects.all().count()
   total_flats = flat.objects.all().count()
   total_villas = villa.objects.all().count()
   total_plots = plot.objects.all().count()
   total_shops = commercial_shop.objects.all().count()
   total_expenses = society_expense.objects.all().count()
   
   context = {
      'total_clients':total_clients,
      'total_societies':total_societies,
      'total_flats':total_flats,
      'total_villas':total_villas,
      'total_plots':total_plots,
      'total_shops':total_shops,
      'total_expenses':total_expenses,
   }
   return render(request, "crm/dashboard.html", context)

@login_required(login_url='/')
def my_profile(request, id):
   profile = CustomUser.objects.get(pk=id)
   print(profile)
   ProfileForm = forms.ClientUserForm(instance=profile)
   if request.method == 'POST':
      ProfileForm = forms.ClientUserForm(request.POST, instance=profile)
      if ProfileForm.is_valid():
         ProfileForm.save()
         return HttpResponseRedirect('/dashboard/')

   context = {'ProfileForm':ProfileForm}
   return render(request, 'crm/my_profile.html', context)

"""
==================================================================
 Client Related views
==================================================================
"""

@login_required(login_url='/')
def client_dashboard(request):

   return render(request, 'crm/client_dashboard.html')

@login_required(login_url='/')
def new_client(request):
   ClientUserForm = forms.ClientUserForm()
   ClientForm = forms.ClientForm()
   if request.method=='POST':
      ClientUserForm = forms.ClientUserForm(request.POST)
      ClientForm = forms.ClientForm(request.POST)
      UserType = request.POST.get('user_type')
      print(request.POST.get('user_type'))
      if ClientUserForm.is_valid() and ClientForm.is_valid():
         if UserType=='Role Based User':
            user = ClientUserForm.save(commit=False)
            user.contact=request.POST.get('mobile_number')
            user.email = request.POST.get('email_address')
            user.save()
            client = ClientForm.save(commit=False)
            client.user=user
            client.save()

            messages.success(request,"New Role Based User has been created successfully!!")   
               
         client = ClientForm.save(commit=False)
         client.save()

   context = {'ClientUserForm':ClientUserForm, 'ClientForm':ClientForm}

   return render(request, 'crm/new_client.html', context=context)


@login_required(login_url='/')
def new_caretaker(request):
   CaretakerForm = forms.ClientUserForm()
   if  request.method == 'POST':
      CaretakerForm = forms.ClientUserForm(request.POST)

      if CaretakerForm.is_valid():
         user =  CaretakerForm.save()
         caretaker_group = Group.objects.get_or_create(name='caretaker')
         caretaker_group[0].user_set.add(user)
         CaretakerForm.save()
         messages.success(request,"New Caretaker has been created successfully!!")
         

   return render(request, 'crm/caretaker.html', {'CaretakerForm':CaretakerForm})

def assign_property_view(request):
   AssignedPropertyForm = forms.AssignedPropertyForm()
   if request.method=='POST':
      AssignedPropertyForm = forms.AssignedPropertyForm(request.POST)
      if AssignedPropertyForm.is_valid():
         AssignedPropertyForm.save()
         messages.success(request,"Property has been Assigned successfully!!")
   context = {'AssignedPropertyForm':AssignedPropertyForm}
   return render(request, 'crm/assign_property.html', context)
   

@login_required(login_url='/')
def view_all_client(request):
   clients = client.objects.all()
   
   context = {'clients':clients}
   return render(request, 'crm/view_all_client.html', context)

"""
======================================================================
Role Related Views
======================================================================
"""

@login_required(login_url='/')
def new_role(request):
   if request.method == 'POST':
      role = request.POST.get('role')      
      role_group = Group.objects.get_or_create(name=role)

      messages.success(request,"New Role has been created successfully!!")

   return render(request, 'crm/new_role.html')

@login_required(login_url='/')
def assign_role(request):
   role_based_user = client.objects.all()
   roles = Group.objects.all()
   societies = society.objects.all()
   context = {
      'role_based_user':role_based_user,
      'roles':roles,
      'societies':societies,
      }
   return render(request, 'crm/assign_role.html', context)

def view_roles(request):

   return render(request, 'crm/view_roles.html')

"""
======================================================================
Society Related Views
======================================================================
"""

@login_required(login_url='/')
def society_dashboard(request):

   return render(request, 'crm/society_dashboard.html')

@login_required(login_url='/')
def new_society(request):
   SocietyForm = forms.SocietyForm()
   if request.method == 'POST':
      SocietyForm = forms.SocietyForm(request.POST, request.FILES)
      if SocietyForm.is_valid():
         SocietyForm.save()
         messages.success(request,"New Society has been created successfully!!")
   return render(request, 'crm/new_society.html', {'SocietyForm':SocietyForm})

@login_required(login_url='/')
def view_society(request):
   societies = society.objects.all()

   return render(request, 'crm/view_society.html', {'societies':societies})

@login_required(login_url='/')
def edit_society(request,id):
   society_name = society.objects.get(id=id)
   SocietyForm = forms.SocietyForm(instance=society_name)
   if request.method=='POST':
      SocietyForm = forms.SocietyForm(request.POST, request.FILES, instance=society_name)
      if SocietyForm.is_valid():
         SocietyForm.save()
         messages.success(request, "Society Updated Successfully!!")
         return HttpResponseRedirect('/society/society-view/')
   context = {'SocietyForm':SocietyForm}
   return render(request, 'crm/edit_society.html', context)

@login_required(login_url='/')
def new_block(request):
   societies = society.objects.all()
   print(request.method)
   if request.method == "POST":

      lenth =  request.POST.get('totallength')
      
      if lenth == '':
         lenth = 1
      else :
         lenth = int(lenth)+1
      
      sty = request.POST.get("society" , None)
      sty = society.objects.get(society_title = sty)
      # print(sty[0].id)
      for i in range(lenth) :
         try:
            blc = request.POST.get("block"+str(i))
            print(blc,sty)
            block.objects.create(society=sty , block=blc)
         except :
            pass


      messages.success(request ,"New Block has been created successfully!!" )

   
   return render(request, 'crm/new_block.html', {'stss':societies})

@login_required(login_url='/')
def view_blocks(request):
   all_blocks = block.objects.all()   
   return render(request, 'crm/view_blocks.html', {'all_blocks':all_blocks})

@login_required(login_url='/')
def edit_block(request, id):
   block_name = block.objects.get(id=id)
   BlockEditForm = forms.BlockForm(instance=block_name)
   if request.method == 'POST':
      BlockEditForm = forms.BlockForm(request.POST, instance=block_name)
      if BlockEditForm.is_valid():
         BlockEditForm.save()
         return HttpResponseRedirect('/society/blocks-view/')
   context = {'BlockEditForm':BlockEditForm}
   return render(request, 'crm/edit_block.html', context)

@login_required(login_url='/')
def new_floor(request):
   FloorForm = forms.FloorForm()
   if request.method == 'POST':
      FloorForm = forms.FloorForm(request.POST)
      if FloorForm.is_valid():
         FloorForm.save()
         messages.success(request,"New Floor has been created successfully!!")
   return render(request, 'crm/new_floor.html', {'FloorForm':FloorForm})

@login_required(login_url='/')
def view_floors(request):
   floors = floor.objects.all()   
   return render(request, 'crm/view_floors.html', {'floors':floors})

@login_required(login_url='/')
def edit_floor(request, id):
   floor_name = floor.objects.get(id=id)
   FloorForm = forms.FloorForm(instance=floor_name)
   if request.method == 'POST':
      FloorForm = forms.FloorForm(request.POST, instance=floor_name)
      if FloorForm.is_valid():
         FloorForm.save()
         messages.success(request, "Floor Updated Successfully!!")
         return HttpResponseRedirect('/society/floor-view/')
   context = {'FloorForm':FloorForm}
   return render(request, 'crm/edit_floor.html', context)

"""
======================================================================
Society-category Related Views
======================================================================
"""
@login_required(login_url='/')
def society_category_dashboard(request):

   return render(request, 'crm/society_category_dashboard.html')

@login_required(login_url='/')
def new_flat(request):
   FlatForm = forms.FlatForm()
   if request.method=='POST':
      FlatForm = forms.FlatForm(request.POST)
      if FlatForm.is_valid():
         FlatForm.save()
         messages.success(request,"New Flat has been created successfully!!")
   return render(request, 'crm/new_flat.html', {'FlatForm':FlatForm})

@login_required(login_url='/')
def view_flats(request):
   f = flat.objects.all()
   flats = filters.SocietyFilter(request.GET, queryset=f)
   return render(request, 'crm/view_flats.html', {'flats':f})

@login_required(login_url='/')
def edit_flat(request, id):
   flat_name = flat.objects.get(id=id)
   FlatForm = forms.FlatForm(instance=flat_name)
   if request.method=='POST':
      FlatForm = forms.FlatForm(request.POST, instance=flat_name)
      if FlatForm.is_valid():
         FlatForm.save()
         messages.success(request,"Flat has been updated successfully!!")
   return render(request, 'crm/edit_flat.html', {'FlatForm':FlatForm})

@login_required(login_url='/')
def new_villa(request):
   VillaForm = forms.VillaForm()
   if request.method=='POST':
      VillaForm = forms.VillaForm(request.POST)
      if VillaForm.is_valid():
         VillaForm.save()
         messages.success(request,"New Villa has been created successfully!!")
   return render(request, 'crm/new_villa.html', {'VillaForm':VillaForm})

@login_required(login_url='/')
def view_villas(request):
   villas = villa.objects.all()

   return render(request, 'crm/view_villas.html', {'villas':villas})   

@login_required(login_url='/')
def edit_villa(request, id):
   villa_name = villa.objects.get(id=id)
   VillaForm = forms.VillaForm(instance=villa_name)
   if request.method=='POST':
      VillaForm = forms.VillaForm(request.POST, instance=villa_name)
      if VillaForm.is_valid():
         VillaForm.save()
         messages.success(request,"Villa has been Updated successfully!!")
   return render(request, 'crm/edit_villa.html', {'VillaForm':VillaForm})

@login_required(login_url='/')
def new_plot(request):
   PlotForm = forms.PlotForm()
   if request.method=='POST':
      PlotForm = forms.PlotForm(request.POST)
      if PlotForm.is_valid():
         PlotForm.save()
         messages.success(request,"New Plot has been created successfully!!")
   return render(request, 'crm/new_plot.html', {'PlotForm':PlotForm})

@login_required(login_url='/')
def edit_plot(request, id):
   plot_name = plot.objects.get(id=id)
   PlotForm = forms.PlotForm(instance = plot_name)
   if request.method=='POST':
      PlotForm = forms.PlotForm(request.POST, instance = plot_name)
      if PlotForm.is_valid():
         PlotForm.save()
         messages.success(request,"Plot has been Updated successfully!!")
   return render(request, 'crm/edit_plot.html', {'PlotForm':PlotForm})

@login_required(login_url='/')
def view_plots(request):
   plots = plot.objects.all()

   return render(request, 'crm/view_plots.html', {'plots':plots})

@login_required(login_url='/')
def new_shop(request):
   ShopForm = forms.ShopForm()
   if request.method=='POST':
      ShopForm = forms.ShopForm(request.POST)
      if ShopForm.is_valid():
         ShopForm.save()
         messages.success(request,"New Shop has been created successfully!!")
   return render(request, 'crm/new_shop.html', {'ShopForm':ShopForm})

@login_required(login_url='/')
def edit_shop(request, id):
   shop_name = commercial_shop.objects.get(id=id)
   ShopForm = forms.ShopForm(instance=shop_name)
   if request.method=='POST':
      ShopForm = forms.ShopForm(request.POST, instance=shop_name)
      if ShopForm.is_valid():
         ShopForm.save()
         messages.success(request,"Shop has been updated successfully!!")
   return render(request, 'crm/edit_shop.html', {'ShopForm':ShopForm})

@login_required(login_url='/')
def view_shops(request):
   shops = commercial_shop.objects.all()

   return render(request, 'crm/view_shops.html', {'shops':shops})

"""
======================================================================
Society-Expense Management Related Views
======================================================================
"""

@login_required(login_url='/')
def society_expense_dashboard(request):

   return render(request, 'crm/society_expense_dashboard.html')

@login_required(login_url='/')
def new_society_expense(request):
   SocietyExpenseForm = forms.SocietyExpenseForm()
   if request.method=='POST':
      SocietyExpenseForm = forms.SocietyExpenseForm(request.POST, request.FILES)
      if SocietyExpenseForm.is_valid():
         SocietyExpenseForm.save()
         messages.success(request,"New Society Expense has been created successfully!!")
   context={
      'SocietyExpenseForm':SocietyExpenseForm
   }
   return render(request, 'crm/new_society_expense.html', context)

@login_required(login_url='/')
def edit_society_expense(request, id):
   expense = society_expense.objects.get(id=id)
   SocietyExpenseForm = forms.SocietyExpenseForm(instance=expense)
   if request.method=='POST':
      SocietyExpenseForm = forms.SocietyExpenseForm(request.POST, request.FILES, instance=expense)
      if SocietyExpenseForm.is_valid():
         SocietyExpenseForm.save()
         messages.success(request,"Society Expense has been updated successfully!!")
   context={
      'SocietyExpenseForm':SocietyExpenseForm
   }
   return render(request, 'crm/edit_society_expense.html', context)

@login_required(login_url='/')
def view_society_expenses(request):
   society_expenses = society_expense.objects.all()
   context = {'society_expenses':society_expenses}
   return render(request, 'crm/view_society_expense.html', context)

"""
======================================================================
Society-Rental Related Views
======================================================================
"""

@login_required(login_url='/')
def rental_dashboard(request):

   return render(request, 'crm/rental_dashboard.html')

@login_required(login_url='/')
def rental_allotment(request):
   RentalForm = forms.RentalForm()
   if request.method=='POST':
      RentalForm = forms.RentalForm(request.POST)
      if RentalForm.is_valid():
         RentalForm.save()
         messages.success(request,"Rent has been Alloted successfully!!")
   context = {'RentalForm':RentalForm}
   return render(request, 'crm/rental_allotment.html', context)

@login_required(login_url='/')
def rental_edit(request, id):
   rent = rental.objects.get(id=id)
   RentalForm = forms.RentalForm(instance=rent)
   if request.method=='POST':
      RentalForm = forms.RentalForm(request.POST, instance=rent)
      if RentalForm.is_valid():
         RentalForm.save()
         messages.success(request,"Ret has been Updated successfully!!")
   context = {'RentalForm':RentalForm}
   return render(request, 'crm/edit_rental.html', context)

@login_required(login_url='/')
def view_rental(request):
   all_rents = rental.objects.all()
   context = {'all_rents':all_rents}   
   return render(request, 'crm/view_rental.html', context)

"""
======================================================================
Society-Finance and Reporting Related Views
======================================================================
"""
@login_required(login_url='/')
def finance_dashboard(request):

   return render(request, 'crm/finance_dashboard.html')

@login_required(login_url='/')
def demand_creation_view(request):
   DemandCreationForm = forms.DemandCreationForm()
   if request.method=='POST':
      DemandCreationForm = forms.DemandCreationForm(request.POST)
      if DemandCreationForm.is_valid():
         DemandCreationForm.save()
         messages.success(request,"New Demand has been created successfully!!")
   context = {'DemandCreationForm':DemandCreationForm}
   return render(request, 'crm/demand_creation.html', context)

@login_required(login_url='/')
def demand_edit_view(request, id):
   demand = CAM_demand.objects.get(id=id)
   DemandCreationForm = forms.DemandCreationForm(instance=demand)
   if request.method=='POST':
      DemandCreationForm = forms.DemandCreationForm(request.POST, instance=demand)
      if DemandCreationForm.is_valid():
         DemandCreationForm.save()
         messages.success(request,"Demand has been updated successfully!!")
   context = {'DemandCreationForm':DemandCreationForm}
   return render(request, 'crm/edit_demand.html', context)

@login_required(login_url='/')
def cam_demand(request):
   cam_demands = CAM_demand.objects.all()

   return render(request, 'crm/cam_demand.html', {'demands':cam_demands})

@login_required(login_url='/')
def cam_calculation_rented_add(request):
   CamCalculationForm = forms.CamCalculationForm()
   if request.method=='POST':
      CamCalculationForm = forms.CamCalculationForm(request.POST)
      if CamCalculationForm.is_valid():
         CamCalculationForm.save()
   context = {'CamCalculationForm':CamCalculationForm}
   return render(request, 'crm/new_cam_calculation_rented.html', context)

@login_required(login_url='/')
def cam_calculation_rented_edit(request, id):
   cam = CAM_calculation.objects.get(id=id)
   CamCalculationForm = forms.CamCalculationForm(instance=cam)
   if request.method=='POST':
      CamCalculationForm = forms.CamCalculationForm(request.POST, instance=cam)
      if CamCalculationForm.is_valid():
         CamCalculationForm.save()
   context = {'CamCalculationForm':CamCalculationForm}
   return render(request, 'crm/edit_cam_calculation_rented.html', context)

@login_required(login_url='/')
def cam_calculation_rented_view(request):
   calculations = CAM_calculation.objects.all()
   context={'calculations':calculations}
   return render(request, 'crm/view_cam_calculation_rented.html', context)

@login_required(login_url='/')
def cam_calculation_sold_add(request):
   CamCalculationForm = forms.CamCalculationForm()
   if request.method=='POST':
      CamCalculationForm = forms.CamCalculationForm(request.POST)
      if CamCalculationForm.is_valid():
         CamCalculationForm.save()
   context = {'CamCalculationForm':CamCalculationForm}
   return render(request, 'crm/new_cam_calculation_sold.html', context)

@login_required(login_url='/')
def cam_calculation_sold_edit(request, id):
   cam = CAM_calculation.objects.get(id=id)
   CamCalculationForm = forms.CamCalculationForm(instance=cam)
   if request.method=='POST':
      CamCalculationForm = forms.CamCalculationForm(request.POST, instance=cam)
      if CamCalculationForm.is_valid():
         CamCalculationForm.save()
   context = {'CamCalculationForm':CamCalculationForm}
   return render(request, 'crm/edit_cam_calculation_sold.html', context)

@login_required(login_url='/')
def cam_calculation_sold_view(request):
   calculations = CAM_calculation.objects.all()
   context={'calculations':calculations}
   return render(request, 'crm/view_cam_calculation_sold.html', context)

"""
======================================================================
Recovery Management Related Views
======================================================================
"""

@login_required(login_url='/')
def recovery_management_dashboard(request):

   return render(request, 'crm/recovery_management_dashboard.html')

@login_required(login_url='/')
def recovery_invoice_new(request):
   RecoveryInvoiceForm = forms.RecoveryInvoiceForm()
   if request.method == 'POST':
      RecoveryInvoiceForm = forms.RecoveryInvoiceForm(request.POST, request.FILES)
      if RecoveryInvoiceForm.is_valid():
         RecoveryInvoiceForm.save()
         messages.success(request,"New Invoice has been created successfully!!")
   context = {'RecoveryInvoiceForm':RecoveryInvoiceForm}
   return render(request, 'crm/new_recovery_invoice.html', context)

@login_required(login_url='/')
def recovery_invoice_view(request):
   invoices = invoice.objects.all()

   return render(request, 'crm/view_recovery_invoice.html', {'invoices':invoices})

@login_required(login_url='/')
def recovery_schedule_call_new(request):
   RecoveryScheduleCallForm = forms.RecoveryScheduleCallForm()
   if request.method == 'POST':
      RecoveryScheduleCallForm = forms.RecoveryScheduleCallForm(request.POST)
      if RecoveryScheduleCallForm.is_valid():
         RecoveryScheduleCallForm.save()
         messages.success(request,"New Call has been Scheduled successfully!!")
   context = {'RecoveryScheduleCallForm':RecoveryScheduleCallForm}
   return render(request, 'crm/new_recovery_schedule_call.html', context)

@login_required(login_url='/')
def recovery_schedule_call_view(request):
   schedule_calls = recovery_schedule_call.objects.all()
   context = {'calls':schedule_calls}
   return render(request, 'crm/view_recovery_schedule_calls.html', context)

@login_required(login_url='/')
def recovery_call_followup_new(request):
   RecoveryCallFollowupForm = forms.RecoveryCallFollowupForm()
   if request.method == 'POST':
      RecoveryCallFollowupForm = forms.RecoveryCallFollowupForm(request.POST)
      if RecoveryCallFollowupForm.is_valid():
         RecoveryCallFollowupForm.save()
         messages.success(request,"New Call Followup has been Submitted successfully!!")
   context = {'RecoveryCallFollowupForm':RecoveryCallFollowupForm}
   return render(request, 'crm/new_recovery_followup_call.html', context)

@login_required(login_url='/')
def recovery_call_followup_edit(request, id):
   call = recovery_call_followup.objects.get(id=id)
   RecoveryCallFollowupForm = forms.RecoveryCallFollowupForm(instance=call)
   if request.method == 'POST':
      RecoveryCallFollowupForm = forms.RecoveryCallFollowupForm(request.POST, instance=call)
      if RecoveryCallFollowupForm.is_valid():
         RecoveryCallFollowupForm.save()
         messages.success(request,"Call Followup has been Updated successfully!!")
   context = {'RecoveryCallFollowupForm':RecoveryCallFollowupForm}
   return render(request, 'crm/edit_recovery_followup_call.html', context)

@login_required(login_url='/')
def recovery_call_followup_view(request):
   call_followups = recovery_call_followup.objects.all()
   context={'calls':call_followups}
   return render(request, 'crm/view_recovery_call_followup.html', context)

@login_required(login_url='/')
def recovery_task_new(request):
   RecoveryTaskForm = forms.RecoveryTaskForm()
   if request.method == 'POST':
      RecoveryTaskForm = forms.RecoveryTaskForm(request.POST)
      if RecoveryTaskForm.is_valid():
         RecoveryTaskForm.save()
         messages.success(request,"New Task has been created successfully!!")
   context = {'RecoveryTaskForm':RecoveryTaskForm}
   return render(request, 'crm/new_recovery_task.html', context)

@login_required(login_url='/')
def recovery_task_edit(request, id):
   task = recovery_task.objects.get(id=id)
   RecoveryTaskForm = forms.RecoveryTaskForm(instance=task)
   if request.method == 'POST':
      RecoveryTaskForm = forms.RecoveryTaskForm(request.POST, instance=task)
      if RecoveryTaskForm.is_valid():
         RecoveryTaskForm.save()
         messages.success(request,"Task has been updated successfully!!")
   context = {'RecoveryTaskForm':RecoveryTaskForm}
   return render(request, 'crm/edit_recovery_task.html', context)

@login_required(login_url='/')
def recovery_task_view(request):
   tasks = recovery_task.objects.all()
   return render(request, 'crm/view_recovery_task.html', {'tasks':tasks})

"""
======================================================================
Electricity Related Views
======================================================================
"""
@login_required(login_url='/')
def electricity_bill_society(request):
   ElectricityBillForm = forms.ElectricityBillForm()
   if request.method=='POST':
      ElectricityBillForm = forms.ElectricityBillForm(request.POST)
      if ElectricityBillForm.is_valid():
         ElectricityBillForm.save()
         messages.success(request,"New Bill has been created successfully!!")
   context={
      'ElectricityBillForm':ElectricityBillForm
   }
   return render(request , 'crm/electricity_society.html' , context)


@login_required(login_url='/')
def electricity_bill_client(request):
   ElectricityBillForm = forms.ElectricityBillForm()
   if request.method=='POST':
      ElectricityBillForm = forms.ElectricityBillForm(request.POST)
      if ElectricityBillForm.is_valid():
         ElectricityBillForm.save()
         messages.success(request,"New Bill has been created successfully!!")
   context={
      'ElectricityBillForm':ElectricityBillForm
   }
   return render(request , 'crm/electricity_client.html' , context)

@login_required(login_url='/')
def electricity_bill_view(request):   
   electricity_bills = electricity_bill.objects.all()
   context = {'electricity_bills' : electricity_bills}
   return render(request , 'crm/electricity_view.html' , context)

"""
======================================================================
Water Related Views
======================================================================
"""

@login_required(login_url='/')
def water_society(request):

   WaterBillForm = forms.WaterBillForm()
   if request.method=='POST':
      WaterBillForm = forms.WaterBillForm(request.POST)
      if WaterBillForm.is_valid():
         WaterBillForm.save()
         messages.success(request,"New Bill has been created successfully!!")
   context={
      'WaterBillForm':WaterBillForm
   }
   return render(request , 'crm/water_society.html' , context)


@login_required(login_url='/')
def water_client(request):

   WaterBillForm = forms.WaterBillForm()
   if request.method=='POST':
      WaterBillForm = forms.WaterBillForm(request.POST)
      if WaterBillForm.is_valid():
         WaterBillForm.save()
         messages.success(request,"New Bill has been created successfully!!")
   context={
      'WaterBillForm':WaterBillForm
   }
   return render(request , 'crm/water_client.html' , context)



@login_required(login_url='/')
def water_view(request):
   
   water_bills = water_bill.objects.all()
   context = {'water_bills' : water_bills}
   return render(request , 'crm/water_view.html' , context)



"""
======================================================================
Unit Related Views
======================================================================
"""

@login_required(login_url='/')
def unit_add(request):
   UnitForm = forms.UnitForm()
   if request.method=='POST':
      UnitForm = forms.UnitForm(request.POST)
      if UnitForm.is_valid():
         UnitForm.save()
         messages.success(request,"New Unit has been created successfully!!")
   context={
      'UnitForm':UnitForm
   }
   return render(request, 'crm/unit_add.html', context)

   
@login_required(login_url='/')
def unit_view(request):
   units = unit.objects.all()
   context = {'units' : units}
   return render(request , 'crm/unit_view.html' , context)


@login_required(login_url='/')
def edit_unit(request,id):
   
   unit_ids = unit.objects.get(id=id)
   UnitForm = forms.UnitForm(instance=unit_ids)
   if request.method=='POST':
      UnitForm = forms.UnitForm(request.POST, instance=unit_ids)
      if UnitForm.is_valid():
         UnitForm.save()
         messages.success(request, "Unit Updated Successfully!!")
         return HttpResponseRedirect('/unit/view/')
   context = {'UnitForm':UnitForm}
   return render(request, 'crm/unit_edit.html', context)
   
"""
======================================================================
Discount Related Views
======================================================================
"""

@login_required(login_url='/')
def discount_add(request):
   return render(request , 'crm/discount_add.html')

@login_required(login_url='/')
def discount_society_add(request):
   DiscountSocietyForm = forms.DiscountSocietyForm()
   if request.method=='POST':
      DiscountSocietyForm = forms.DiscountSocietyForm(request.POST, request.FILES)
      if DiscountSocietyForm.is_valid():
         DiscountSocietyForm.save()
         messages.success(request,"New Discount has been Added successfully!!")
   context={
      'DiscountSocietyForm': DiscountSocietyForm
   }
   return render(request, 'crm/discount_society_add.html', context)

@login_required(login_url='/')
def discount_user_add(request):
   DiscountUserForm = forms.DiscountUserForm()
   if request.method=='POST':
      DiscountUserForm = forms.DiscountUserForm(request.POST, request.FILES)
      if DiscountUserForm.is_valid():
         DiscountUserForm.save()
         messages.success(request,"New Discount has been Added successfully!!")
   context={
      'DiscountUserForm': DiscountUserForm
   }
   return render(request, 'crm/discount_user_add.html', context)

@login_required(login_url='/')
def discount_view(request):
   # DiscountView = forms.DiscountView()
   # context = {'DiscountView' : DiscountView}
   # sts = society.objects.values_list('id' , 'society_title')
   sts = society.objects.all()
   bgs = block.objects.all()
   fls = floor.objects.all()
   discount_data = discount_user.objects.all()
   return render(request , 'crm/discount_view.html' , {'sts':sts , 'bgs':bgs , 'fls' : fls , 'discount_data' : discount_data})

@login_required(login_url='/')
def edit_discount(request,id):
   
   discount_ids = discount_user.objects.get(id=id)
   DiscountForm = forms.DiscountUserForm(instance=discount_ids)
   if request.method=='POST':
      DiscountForm = forms.DiscountUserForm(request.POST, request.FILES, instance=discount_ids)
      if DiscountForm.is_valid():
         DiscountForm.save()
         messages.success(request, "Discount User Updated Successfully!!")
         return HttpResponseRedirect('/discount/view/')
   context={
      'DiscountUserForm': DiscountForm
   }
   return render(request, 'crm/discount_user_edit.html', context)
   
"""
======================================================================
report master Related Views
======================================================================
"""

@login_required(login_url='/')
def report_new(request):
   ReportForm = forms.ReportForm()
   if request.method == 'POST':
      ReportForm = forms.ReportForm(request.POST)
      if ReportForm.is_valid():
         ReportForm.save()
         messages.success(request,"New Report has been Created successfully!!")
   context = {'ReportForm':ReportForm}
   return render(request, 'crm/new_report.html', context)

"""
======================================================================
collection master Related Views
======================================================================
"""

@login_required(login_url='/')
def collection_CAM_received_add(request):
   CollectionCAMReceivedForm = forms.CollectionCAMReceivedForm()
   if request.method == 'POST':
      CollectionCAMReceivedForm = forms.CollectionCAMReceivedForm(request.POST)
      if CollectionCAMReceivedForm.is_valid():
         CollectionCAMReceivedForm.save()
         messages.success(request,"New CAM collection has been Added successfully!!")
   context = {'CollectionCAMReceivedForm':CollectionCAMReceivedForm}
   return render(request, 'crm/collection_CAM_received_add.html', context)

@login_required(login_url='/')
def collection_CAM_received_edit(request, id):
   cam_collect = collection_CAM_received.objects.get(id=id)
   CollectionCAMReceivedForm = forms.CollectionCAMReceivedForm(instance=cam_collect)
   if request.method == 'POST':
      CollectionCAMReceivedForm = forms.CollectionCAMReceivedForm(request.POST, instance=cam_collect)
      if CollectionCAMReceivedForm.is_valid():
         CollectionCAMReceivedForm.save()
         messages.success(request,"New CAM collection has been Added successfully!!")
   context = {'CollectionCAMReceivedForm':CollectionCAMReceivedForm}
   return render(request, 'crm/collection_CAM_received_edit.html', context)

@login_required(login_url='/')
def collection_CAM_received_view(request):
   CAM_received = collection_CAM_received.objects.all()
   context = {'CAM_received':CAM_received}
   return render(request, 'crm/collection_CAM_received_view.html', context)

@login_required(login_url='/')
def collection_rent_add(request):
   CollectionRentForm = forms.CollectionRentForm()
   if request.method == 'POST':
      CollectionRentForm = forms.CollectionRentForm(request.POST)
      if CollectionRentForm.is_valid():
         CollectionRentForm.save()
         messages.success(request,"New Rent collection has been Added successfully!!")
   context = {'CollectionRentForm':CollectionRentForm}
   return render(request, 'crm/collection_rent_add.html', context)

@login_required(login_url='/')
def collection_rent_edit(request, id):
   rent = collection_rent.objects.get(id=id)
   CollectionRentForm = forms.CollectionRentForm(instance=rent)
   if request.method == 'POST':
      CollectionRentForm = forms.CollectionRentForm(request.POST, instance=rent)
      if CollectionRentForm.is_valid():
         CollectionRentForm.save()
         messages.success(request,"Rent collection has been Updated successfully!!")
   context = {'CollectionRentForm':CollectionRentForm}
   return render(request, 'crm/collection_rent_edit.html', context)

@login_required(login_url='/')
def collection_rent_view(request):
   rents = collection_rent.objects.all()
   context = {'rents':rents}
   return render(request, 'crm/collection_rent_view.html', context)

@login_required(login_url='/')
def collection_electricity_add(request):
   CollectionElectricityForm = forms.CollectionElectricityForm()
   if request.method == 'POST':
      CollectionElectricityForm = forms.CollectionElectricityForm(request.POST)
      if CollectionElectricityForm.is_valid():
         CollectionElectricityForm.save()
         messages.success(request,"New Electricity bill collection has been Added successfully!!")
   context = {'CollectionElectricityForm':CollectionElectricityForm}
   return render(request, 'crm/collection_electricity_add.html', context)

@login_required(login_url='/')
def collection_electricity_edit(request, id):
   electricity = collection_electricity.objects.get(id=id)
   CollectionElectricityForm = forms.CollectionElectricityForm(instance=electricity)
   if request.method == 'POST':
      CollectionElectricityForm = forms.CollectionElectricityForm(request.POST, instance=electricity)
      if CollectionElectricityForm.is_valid():
         CollectionElectricityForm.save()
         messages.success(request,"Electricity bill collection has been updated successfully!!")
   context = {'CollectionElectricityForm':CollectionElectricityForm}
   return render(request, 'crm/collection_electricity_edit.html', context)

@login_required(login_url='/')
def collection_electricity_view(request):
   electricity_collection = collection_electricity.objects.all()
   context = {'electricity_collection':electricity_collection}
   return render(request, 'crm/collection_electricity_view.html', context)

@login_required(login_url='/')
def collection_water_add(request):
   CollectionWaterForm = forms.CollectionWaterForm()
   if request.method == 'POST':
      CollectionWaterForm = forms.CollectionWaterForm(request.POST)
      if CollectionWaterForm.is_valid():
         CollectionWaterForm.save()
         messages.success(request,"New Water bill collection has been Added successfully!!")
   context = {'CollectionWaterForm':CollectionWaterForm}
   return render(request, 'crm/collection_water_add.html', context)

@login_required(login_url='/')
def collection_water_edit(request, id):
   water = collection_water.objects.get(id=id)
   CollectionWaterForm = forms.CollectionWaterForm(instance=water)
   if request.method == 'POST':
      CollectionWaterForm = forms.CollectionWaterForm(request.POST, instance=water)
      if CollectionWaterForm.is_valid():
         CollectionWaterForm.save()
         messages.success(request,"Water bill collection has been updated successfully!!")
   context = {'CollectionWaterForm':CollectionWaterForm}
   return render(request, 'crm/collection_water_edit.html', context)

@login_required(login_url='/')
def collection_water_view(request):
   water = collection_water.objects.all()
   context = {'water':water}
   return render(request, 'crm/collection_water_view.html', context)

@login_required(login_url='/')
def collection_DG_add(request):
   CollectionDGForm = forms.CollectionDGForm()
   if request.method == 'POST':
      CollectionDGForm = forms.CollectionDGForm(request.POST)
      if CollectionDGForm.is_valid():
         CollectionDGForm.save()
         messages.success(request,"New DG collection has been Added successfully!!")
   context = {'CollectionDGForm':CollectionDGForm}
   return render(request, 'crm/collection_DG_add.html', context)

@login_required(login_url='/')
def collection_DG_edit(request, id):
   dg = collection_DG.objects.get(id=id)
   CollectionDGForm = forms.CollectionDGForm(instance=dg)
   if request.method == 'POST':
      CollectionDGForm = forms.CollectionDGForm(request.POST, instance=dg)
      if CollectionDGForm.is_valid():
         CollectionDGForm.save()
         messages.success(request,"DG collection has been Updated successfully!!")
   context = {'CollectionDGForm':CollectionDGForm}
   return render(request, 'crm/collection_DG_edit.html', context)

@login_required(login_url='/')
def collection_DG_view(request):
   DG_collection = collection_DG.objects.all()
   context = {'DG_collection':DG_collection}
   return render(request, 'crm/collection_DG_view.html', context)

@login_required(login_url='/')
def collection_Income_add(request):
   collection_Income = forms.CollectionIncomeFromFundForm()
   if request.method == 'POST':
      collection_Income = forms.CollectionIncomeFromFundForm(request.POST)
      if collection_Income.is_valid():
         collection_Income.save()
         messages.success(request,"New Fund collection has been Added successfully!!")
   context = {'collection_Income':collection_Income}
   return render(request, 'crm/collection_Income_add.html', context)

@login_required(login_url='/')
def collection_Income_edit(request, id):
   income = collection_Income.objects.get(id=id)
   collection_Income_form = forms.CollectionIncomeFromFundForm(instance=income)
   if request.method == 'POST':
      collection_Income_form = forms.CollectionIncomeFromFundForm(request.POST, instance=income)
      if collection_Income.is_valid():
         collection_Income.save()
         messages.success(request,"Fund collection has been updated successfully!!")
   context = {'collection_Income':collection_Income_form}
   return render(request, 'crm/collection_Income_edit.html', context)

@login_required(login_url='/')
def collection_Income_view(request):
   fund_income = collection_Income.objects.all()
   context = {'fund_income':fund_income}
   return render(request, 'crm/collection_Income_view.html', context)

def delete_me_dash(request):
   return render(request, 'crm/society_dashboard.html')