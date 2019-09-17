from django.urls import path
from book import views


app_name = 'book'
urlpatterns = [
    path('', views.index,name='index'),
    path('result/', views.result, name='result'),
    path('user_info/', views.user_info, name='user_info'),
    path('login_usr/', views.login_usr, name='login_usr'),
    path('logout_usr/', views.logout_usr, name='logout_usr'),
    path('register/', views.register, name = 'register'),
    path('book_flight/<int:flight_id>/',views.book_ticket,name ='book_ticket'),
    path('book_flight_first/<int:flight_id>/',views.book_ticket_firstClass,name ='book_ticket_firstClass'),
    path('refund/<int:flight_id>/',views.refund_ticket,name='refund_ticket'),
    path('delete_payment/<int:bank_account>/',views.delete_payment,name='delete_payment'),
    path('payment/',views.addPayment,name ='addPayment'),
    path('editPayment/',views.editPayment,name='editPayment'),
    path('choosePayment/',views.choosePayment,name='choosePayment'),
    path('orderComplete/',views.orderComplete,name='orderComplete')
]

