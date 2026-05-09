from django.urls import path

from family import views

urlpatterns = [
    path('addmember/',views.addmember,name='addmember'),
    path('familydata/',views.familydata,name='familydata'),
    path('update_member/<int:id>',views.update_data,name='update_member'),
    path('delete_member/<int:id>',views.delete_data,name='delete_member'),
    path('addexpenses/',views.addexpenses,name='addexpenses'),
    path('viewexpenses/',views.viewexpenses,name='viewexpenses'),
    path('update_expense/<int:id>',views.update_expense,name='update_expense'),
    path('delete_expense/<int:id>',views.delete_expense,name='delete_expense'),
    path('monthly/',views.monthly,name='monthly'),
    path('yearly/',views.yearly,name='yearly'),
    path('total/',views.total,name='total'),

]