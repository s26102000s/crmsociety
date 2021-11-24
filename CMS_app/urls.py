from django.urls import path
from django.conf.urls import url
from . import views


app_name = "CMS_app"

urlpatterns = [
   # path("signup/", views.SignUpView, name = "signup"),
   path("", views.LoginView, name = "login"),
   path("logout/", views.LogoutView, name="logout"),
   path("forget-password/", views.forget_pass_view, name="forget_pass"),
   
   path("activate/<uidb64>/<token>", views.activate, name='activate'),
   path("dashboard/", views.dashboard, name="dashboard"),
   path('my-profile/<int:id>/', views.my_profile, name='my_profile'),

   # Client related urls
   path('clients/', views.client_dashboard, name='client_dashboard'),
   path('clients/new/', views.new_client, name='new_client'),
   path('clients/caretaker/', views.new_caretaker, name='caretaker'),
   path('clients/assign-property/', views.assign_property_view, name='assign_property'),
   path('clients/view-all', views.view_all_client, name='view-clients'),
   
   # Role related urls
   path('role/new/', views.new_role, name = 'new_role'),
   path('role/assign/', views.assign_role, name = 'assign_role'),
   path('role/view/', views.view_roles, name = 'view_roles'),

   # Society related urls
   path('society', views.society_dashboard, name='society_dashboard'),
   path('society/society-new/', views.new_society, name='new_society'),
   path('society/society-view/', views.view_society, name='view_society'),
   path('society/society-edit/<int:id>', views.edit_society, name='edit_society'),
   path('society/block-new/', views.new_block, name='new_block'),
   path('society/blocks-view/', views.view_blocks, name='view_blocks'),
   path('society/blocks-edit/<int:id>', views.edit_block, name='edit_block'),
   path('society/floor-new/', views.new_floor, name='new_floor'),
   path('society/floor-view/', views.view_floors, name='view_floors'),
   path('society/floor-edit/<int:id>', views.edit_floor, name='edit_floor'),

   # Society-category related urls
   path('society-category/', views.society_category_dashboard, name = 'society_category_dashboard'),
   path('society-category/flat-new/', views.new_flat, name='new_flat'),
   path('society-category/flats-view/', views.view_flats, name='view_flats'),
   path('society-category/flats-edit/<int:id>', views.edit_flat, name='edit_flat'),
   path('society-category/villa-new/', views.new_villa, name='new_villa'),
   path('society-category/villas-view/', views.view_villas, name='view_villas'),
   path('society-category/villa-edit/<int:id>', views.edit_villa, name='edit_villa'),
   path('society-category/plot-new/', views.new_plot, name='new_plot'),
   path('society-category/plots-view/', views.view_plots, name='view_plots'),
   path('society-category/plot-edit/<int:id>', views.edit_plot, name='edit_plot'),
   path('society-category/shop-new/', views.new_shop, name='new_shop'),
   path('society-category/shops-view/', views.view_shops, name='view_shops'),
   path('society-category/shop-edit/<int:id>', views.edit_shop, name='edit_shop'),

   # Society-expenses related urls
   path('society-expenses/', views.society_expense_dashboard, name='society_expenses_dashboard'),
   path('society-expenses/new/', views.new_society_expense, name='new_society_expense'),
   path('society-expenses/view/', views.view_society_expenses, name='view_society_expenses'),
   path('society-expenses/edit/<int:id>', views.edit_society_expense, name='edit_society_expense'),

   # Society Rental related urls
   path('rental/', views.rental_dashboard, name='rental_dashboard'),
   path('rental/allotment/', views.rental_allotment, name='rental_allotment'),
   path('rental/view/', views.view_rental, name='view_rental'),  
   path('rental/edit/<int:id>', views.rental_edit, name='edit_rental'),  

   # Finance and Reporting Related urls
   path('finance/', views.finance_dashboard, name='finance_dashboard'),
   path('finance/demand-creation', views.demand_creation_view, name = 'demand_creation'),
   path('finance/demand-edit/<int:id>', views.demand_edit_view, name = 'edit_demand'),
   path('finance/cam-demand', views.cam_demand, name = 'cam_demand'),
   path('finance/cam-calculation/rented/add/', views.cam_calculation_rented_add, name = 'cam_calculation_rented_add'),
   path('finance/cam-calculation/rented/edit/<int:id>', views.cam_calculation_rented_edit, name = 'cam_calculation_rented_edit'),
   path('finance/cam-calculation/rented/view/', views.cam_calculation_rented_view, name = 'cam_calculation_rented_view'),
   path('finance/cam-calculation/sold/add/', views.cam_calculation_sold_add, name = 'cam_calculation_sold_add'),
   path('finance/cam-calculation/sold/edit/<int:id>', views.cam_calculation_sold_edit, name = 'cam_calculation_sold_edit'),
   path('finance/cam-calculation/sold/view/', views.cam_calculation_sold_view, name = 'cam_calculation_sold_view'),

   # Recovery management related urls
   path('recovery/', views.recovery_management_dashboard, name = 'recovery_management_dashboard'),
   path('recovery/invoice-new', views.recovery_invoice_new, name = 'recovery_invoice_new'),
   path('recovery/invoice-view', views.recovery_invoice_view, name = 'recovery_invoice_view'),
   path('recovery/schedule-call-new/', views.recovery_schedule_call_new, name = 'recovery_schedule_call_new'),
   path('recovery/schedule-call-view/', views.recovery_schedule_call_view, name = 'recovery_schedule_call_view'),
   path('recovery/call-follow-up-new/', views.recovery_call_followup_new, name = 'recovery_call_followup_new'),
   path('recovery/call-follow-up-view/', views.recovery_call_followup_view, name = 'recovery_call_followup_view'),
   path('recovery/call-follow-up-edit/<int:id>', views.recovery_call_followup_edit, name = 'recovery_call_followup_edit'),
   path('recovery/task-new/', views.recovery_task_new, name='recovery_task_new'),
   path('recovery/task-view/', views.recovery_task_view, name='recovery_task_view'),
   path('recovery/task-edit/<int:id>', views.recovery_task_edit, name='recovery_task_edit'),

   #Electricity Bill
   path('electricity', views.delete_me_dash, name='electricity_dashboard'),
   path('electricity-bill/society/' , views.electricity_bill_society , name='electricity_bill_society' ),
   path('electricity-bill/client/' , views.electricity_bill_client , name='electricity_bill_client' ),
   path('electricity-bill/view/' , views.electricity_bill_view , name='electricity_bill_view' ),

   #Water URLs
   path('water', views.delete_me_dash, name='water_dashboard'),
   path('water/society/' , views.water_society , name='water_society' ),
   path('water/client/' , views.water_client , name='water_client' ),
   path('water/view/' , views.water_view , name='water_view' ),

   #Discount Master
   path('discount/add/' , views.discount_add , name='discount_add' ) ,
   path('discount/add/userSpecific/' , views.discount_user_add , name='discount_user_add' ) ,
   path('discount/add/society/' , views.discount_society_add , name='discount_society_add' ) ,
   path('discount/view/' , views.discount_view , name='discount_view' ) ,
   path('discount/discount-edit/<int:id>', views.edit_discount, name='edit_discount'),



   #Unit Master
   path('unit/add/' , views.unit_add , name='unit_add' ) ,
   path('unit/view/' , views.unit_view , name='unit_view' ),
   path('unit/unit-edit/<int:id>', views.edit_unit , name='edit_unit'),

   #report-master related urls
   path('report/new/', views.report_new, name='report_new'),

   #collection-master related urls
   path('collection/', views.delete_me_dash, name='collection_dashboard'),
   path('collection-CAM-received/add/', views.collection_CAM_received_add, name='collection_CAM_received_add'),
   path('collection_CAM_received/view/', views.collection_CAM_received_view, name='collection_CAM_received_view'),
   path('collection_CAM_received/edit/<int:id>', views.collection_CAM_received_edit, name='collection_CAM_received_edit'),

   path('collection-rent/add/', views.collection_rent_add, name='collection_rent_add'),
   path('collection-rent/view/', views.collection_rent_view, name='collection_rent_view'),
   path('collection-rent/edit/<int:id>', views.collection_rent_edit, name='collection_rent_edit'),

   path('collection-electricity/add/', views.collection_electricity_add, name='collection_electricity_add'),
   path('collection-electricity/view/', views.collection_electricity_view, name='collection_electricity_view'),
   path('collection-electricity/edit/<int:id>', views.collection_electricity_edit, name='collection_electricity_edit'),

   path('collection-water/add/', views.collection_water_add, name='collection_water_add'),
   path('collection-water/view/', views.collection_water_view, name='collection_water_view'),
   path('collection-water/edit/<int:id>', views.collection_water_edit, name='collection_water_edit'),

   path('collection-DG/add/', views.collection_DG_add, name='collection_DG_add'),
   path('collection-DG/view/', views.collection_DG_view, name='collection_DG_view'),
   path('collection-DG/edit/<int:id>', views.collection_DG_edit, name='collection_DG_edit'),

   path('collection_Income_add/', views.collection_Income_add, name='collection_Income_add'),
   path('collection_Income_view/', views.collection_Income_view, name='collection_Income_view'),
   path('collection_Income_edit/<int:id>', views.collection_Income_edit, name='collection_Income_edit'),
]