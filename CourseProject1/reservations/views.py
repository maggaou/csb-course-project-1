from django.shortcuts import render, redirect
from django.contrib import messages
from requests import Session
from reservations.forms import LogInForm, RegisterForm, ReservationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from reservations.models import Reservation
from django.contrib.auth.decorators import login_not_required
from django.views.decorators.debug import sensitive_post_parameters
from django.core.cache import cache
from django.conf import settings

def index(request):
    context = {
        "user": request.user,
        "reservations": []
    }
    if request.user.is_authenticated:
        context["reservations"] = Reservation.objects.filter(owner = request.user)
    return render(request, 'reservations/index.html', context)

# @login_not_required # flaw 1
def loginView(request):
    if request.user.is_authenticated:
        return redirect('/reservations')
    
    next = request.POST.get("next")

    if request.method == 'POST': # form submission
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            # display error message if username is not found
            messages.error(request, 'User is not found') 
            return redirect('/reservations/login')
        
        # login attempt, returns None if unsuccesful (password try)
        user = authenticate(username=username, password=password, request=request)

        # check if login is ip-banned (FLAW 4)

        ip = get_ip_address(request)
        key = f'failed_login_attempts_{ip}'
        attempts = cache.get(key,0)
        if attempts >= settings.MAX_FAILED_LOGIN_ATTEMPTS:
            messages.error(request, "Your IP has been temporarily locked due to multiple failed login attempts.")
            return redirect('/reservations/login')

        if user is None:
            messages.error(request, "Wrong password")

            # failed login attempt will increase failed_login_attempts
            # cache.set(key,attempts+1,timeout=settings.FAILED_LOGIN_LOCK_DURATION)

            return redirect('/reservations/login')
        else:
            messages.success(request, 'Login ok')
            login(request, user)

            # successful login will reset the failed_login_attempts
            cache.delete(key)

            if next:
                return redirect(next)
            else:
                return redirect("/reservations")
            
    context ={}
    context['form']= LogInForm()
    return render(request, 'reservations/login.html', context)

def createReservation(request):
    if request.method == 'POST': # form submission
        form = ReservationForm(request.POST)
        # is valid form?
        if form.is_valid():
            user = request.user
            date = form.cleaned_data["date"]
            participants = form.cleaned_data["numberOfparticipants"]
            details = form.cleaned_data["details"]
            duration = form.cleaned_data["duration"]

            res = Reservation(owner=user,date=date,duration=duration,numberOfparticipants=participants,details=details)
            res.save()
            messages.info(request, "Reservation created")
            return redirect("/reservations/add")
        else:
            messages.error(request, "Invalid details")
            return render(request, "add_reservation.html", {"form": form})
    
    form = ReservationForm()
    edit = False
    if request.GET.get("id"): # editing existing reservation (preparing view)
        edit = True
        request.session["edit"] = True
        id = int(request.GET.get("id"))
        try:
            res = Reservation.objects.get(id = id)
        except Reservation.DoesNotExist:
            return cheaterView(request)
        request.session["id"] = id
        form = ReservationForm(instance=res)
    return render(request, 'reservations/add_reservation.html', {"form": form, "edit": edit})

def createUser(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'reservations/register.html', {'form': form})
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,"User was created")
            login(request, user)
            return redirect("/reservations")
        else:
            return render(request, 'reservations/register.html', {'form': form})

def viewReservation(request):
    if request.method == 'GET':
        id = int(request.GET.get("id"))
        res = Reservation.objects.get(id = id)
        # if res.owner != request.user:                             ######### FLAW 2
        #     return render(request, 'reservations/cheater.html')
        return render(request, 'reservations/view_reservation.html', {"reservation": res})
    
def editReservation(request):
    if request.method == 'POST':
        if request.session["edit"] and request.session["id"]:
            res = Reservation.objects.get(id = request.session["id"])

            form = ReservationForm(request.POST, instance=res)
            form.save()
            messages.info(request, "Reservation updated")
            return render(request, 'reservations/view_reservation.html', {"reservation": res})
        else:
            messages.error(request, "Error")
    return redirect('/reservations')


def cheaterView(request):
	return render(request, 'pages/cheater.html')

def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip