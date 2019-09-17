from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Flight, Customer, Payment, Flight_order
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from operator import attrgetter
import datetime, pytz
from .forms import PassengerInfoForm, UserForm,PaymentForm
from django.contrib.auth.models import Permission, User
from .classes import Order


def index(request):
    return render(request, 'page/index.html')



def user_info(request):
    if request.user.is_authenticated:
        booked_flight = Flight_order.objects.filter(email=request.user.email)
        email = request.user.email
        person = Customer.objects.get(email=email)
        payment = Payment.objects.filter(email=email)
        context = {
            'booked_flight': booked_flight,
            'username':request.user.username,
            'distance': person.distance,
            'payment': payment
        }

        return render(request,'page/user_info.html',context)
    return render(request,'page/login.html')



def login_usr(request):
    if request.method == 'POST':
        username = request.POST.get('username',False)
        password = request.POST.get('password',False)
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            context = {
                'username': request.user.username
            }
            if user.username == 'admin':
                print("hello")
                context = admin_finance(request)
                return render(request,'page/admin.html',context)
            return render(request,'page/result.html',context)

        else:
            return render(request, 'page/login.html', {'error_message': 'Invalid login'})
    return render(request, 'page/login.html')


def admin_finance(request):
    all_flights = Flight_order.objects.all()
    all_flights = sorted(all_flights,key=attrgetter('departure_time'))

    all_passengers = User.objects.exclude(pk=7)
    # print(all_passengers)

    order_list = set()
    for p in all_passengers:
        flights = Flight_order.objects.filter(email=p.email)
        if flights:
           for flight in flights:
               route = flight.departure_city + '->' + flight.arrive_city
               order = Order(p.username,flight.name,route,flight.departure_time,flight.price, flight.payment)
               order_list.add(order)

    context = {
        "order_set": order_list
    }

    return context

def logout_usr(request):

    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'page/login.html', context)



def book_ticket_firstClass(request,flight_id):
    if not request.user.is_authenticated:
        return render(request,'page/login.html')

    else:
        flight = Flight.objects.get(pk= flight_id)
        booked_flight = Flight.objects.filter(user=request.user)


        if flight in booked_flight:
            return render(request,'page/book_conflict.html')


        if flight.capacity > 0:
            flight.book_sum +=1
            flight.capacity -=1
            flight.user.add(request.user)
            flight.save()

        email = request.user.email
        person = Customer.objects.get(email=email)
        person.distance += flight.distance
        person.save()

        flight_order = Flight_order()
        flight_order.id = flight.id
        flight_order.email = request.user.email
        flight_order.name = flight.name
        flight_order.capacity = flight.first_capacity
        flight_order.book_sum = flight.first_book_sum
        flight_order.price = flight.first_price
        flight_order.distance = flight.distance
        flight_order.departure_city = flight.departure_city
        flight_order.arrive_city = flight.arrive_city
        flight_order.departure_time = flight.departure_time
        flight_order.departure_airport = flight.departure_airport
        flight_order.arrive_airport = flight.arrive_airport
        flight_order.arrive_time = flight.arrive_time
        flight_order.save()

        payments = Payment.objects.filter(email=request.user.email)

        context = {
            'flight': flight_order,
            'username': request.user.username,
            'payments': payments
        }

        return render(request,'page/book_flight_first.html',context)


def book_ticket(request,flight_id):
    if not request.user.is_authenticated:
        return render(request,'page/login.html')

    else:
        flight = Flight.objects.get(pk= flight_id)
        booked_flight = Flight.objects.filter(user=request.user)



        if flight in booked_flight:
            return render(request,'page/book_conflict.html')


        if flight.capacity > 0:
            flight.book_sum +=1
            flight.capacity -=1
            flight.user.add(request.user)
            flight.save()

        email = request.user.email
        person = Customer.objects.get(email=email)
        person.distance += flight.distance
        person.save()


        flight_order = Flight_order()
        flight_order.id = flight.id
        flight_order.email = request.user.email
        flight_order.book_sum = flight.book_sum
        flight_order.name = flight.name
        flight_order.capacity = flight.capacity
        flight_order.price = flight.price
        flight_order.distance = flight.distance
        flight_order.departure_city = flight.departure_city
        flight_order.arrive_city = flight.arrive_city
        flight_order.departure_time = flight.departure_time
        flight_order.departure_airport = flight.departure_airport
        flight_order.arrive_airport = flight.arrive_airport
        flight_order.arrive_time = flight.arrive_time
        flight_order.save()


        payments = Payment.objects.filter(email=request.user.email)


        context = {
            'flight': flight_order,
            'username': request.user.username,
            'payments': payments
        }

        return render(request,'page/book_flight.html',context)



def refund_ticket(request,flight_id):
    flight = Flight.objects.get(pk = flight_id)
    flight.book_sum -=1
    flight.capacity +=1
    flight.user.remove(request.user)
    flight.save()
    flight_order = Flight_order.objects.get(pk=flight_id,email=request.user.email)
    flight_order.delete()

    email = request.user.email
    person = Customer.objects.get(email=email)
    person.distance -= flight.distance
    person.save()
    return HttpResponseRedirect('/user_info')


def delete_payment(request,bank_account):
    payment = Payment.objects.get(bank_account=bank_account,email=request.user.email)
    payment.delete()
    return HttpResponseRedirect('/editPayment')



def addPayment(request):
    if request.method == 'POST':
        account = request.POST.get('bank_account',False)
        email = request.user.email
        payment = Payment()
        payment.email = email
        payment.bank_account = account
        payment.save()

    return HttpResponseRedirect('/editPayment')


def editPayment(request):
    if request.user.is_authenticated:
        email = request.user.email
        payment = Payment.objects.filter(email=email)
        context = {
            'payments': payment
        }
        return render(request,'page/payment.html', context)

    return render(request,'page/login.html')

def choosePayment(request):
    if request.method == 'POST':
        account = request.POST.get('bank_account',False)
        flight = Flight_order.objects.last()
        flight.payment = account
        flight.save()


    return render(request,'page/orderComplete.html')


def register(request):
    form = UserForm(request.POST or None)
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user.set_password(password)
            user.save()
            user = authenticate(username=username,password=password)
            cusomer = Customer(email = email,name=username,distance=0)
            cusomer.save()

            if user is not None:
                login(request,user)
                context = {
                    'username': request.user.username
                }
                return render(request,'page/result.html',context)

    context = {
        'form': form
    }
    return render(request,'page/register.html',context)




def orderComplete(request):
    return render(request,'page/orderComplete.html')



def result(request):

    # get request.post and pass form values into PassengerInfoForm
    if request.method == 'POST':
        form = PassengerInfoForm(request.POST)
        if form.is_valid():
            passenger_lcity = form.cleaned_data.get('departure_city')
            passenger_acity = form.cleaned_data.get('arrive_city')
            passenger_ldate = form.cleaned_data.get('departure_date')
            passenger_ltime = datetime.datetime.combine(passenger_ldate, datetime.time())


            # find available flight
            all_flight = Flight.objects.all().filter(departure_city=passenger_lcity,arrive_city=passenger_acity)
            available_flight = []
            for flight in all_flight:
                flight.departure_time = flight.departure_time.replace(tzinfo=None)
                departure_date = flight.departure_time
                departure_date = departure_date.strftime("%Y-%m-%d")
                if departure_date == str(passenger_ldate):
                    available_flight.append(flight)


            available_flight_by_price = sorted(available_flight, key=attrgetter('price'))

            # convert datetime to str
            time_format = "%H:%M"
            for flight in available_flight:
                flight.departure_time = flight.departure_time.strftime(time_format)
                flight.arrive_time = flight.arrive_time.strftime(time_format)


            dis_search_head = 'block'
            dis_search_failure = 'none'
            if len(available_flight) == 0:
                dis_search_head = 'none'
                dis_search_failure = 'block'

            context = {
                'departure_city': passenger_lcity,
                'arrive_city': passenger_acity,
                'departure_date': str(passenger_ldate),

                'available_flights_by_price': available_flight_by_price,

                'dis_search_head': dis_search_head,
                'dis_search_failure': dis_search_failure
            }


            if request.user.is_authenticated:
                if request.user.username == 'admin':
                    context = admin_finance(request)
                    return render(request,'page/admin.html',context)
                else:
                    context['username'] = request.user.username
            return render(request, 'page/result.html', context)
        else:
            return render(request,'page/index.html')


    else:
        context = {
            'dis_search_head': 'none',
            'dis_search_failure': 'none'
        }
        return render(request, 'page/register.html',context)














