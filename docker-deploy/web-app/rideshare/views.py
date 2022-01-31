from re import template
from sre_constants import SUCCESS
from django.shortcuts import render, redirect
from django.http import HttpResponse,  HttpResponseRedirect, request
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.contrib.auth.models import User
from rideshare.models import *
from rideshare.forms import *
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.shortcuts import get_object_or_404
from django.db.models import Q

# WELCOME PAGE
def index(request):
    return render(request, "rideshare/index.html")

# Login page for register user of the rideshare app
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("rideshare:home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "rideshare/login.html", {"form":form})

# Page to register/create an account as a user of the rideshare app
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Successfully registered the user!" )
            return redirect("rideshare:login")
        messages.error(request, "Registration failed! Invalid information.")
    form = UserRegisterForm()
    return render (request, "rideshare/register.html", {"form": form})

# Log-out page
def logout(request):
    auth_logout(request)
    redirect("rideshare:index")

#Home Page for ride owner, a button to request new ride and a list of all the open ride
@login_required(login_url="rideshare:login")
def ridehome(request):
    content={
        'rides':Rides.objects.filter(owner=request.user).filter(Q(status='OP')|Q(status='CF')).order_by('-arrive_date')
    }
    return render(request,"rideshare/ridehome.html",content)


# Ridehistory for all the completed ride
@login_required(login_url="rideshare:login")
def ridehisotry(request):
    content={
        'rides':Rides.objects.filter(owner=request.user).filter(status='CL').order_by('arrive_date')
    }
    return render(request,"rideshare/ride_list.html",content)

#Page for owner view all the rides 
class RideDetailView(LoginRequiredMixin,DetailView):
    model=Rides
    template_name='rideshare/ride_detail.html'


#Page for owner to create a new ride
class RideCreateView(LoginRequiredMixin,CreateView):
    model=Rides
    template_name='rideshare/ride_form.html'
    
    fields=['destination','arrive_date','number_passenger','share','vehicle_type','special_request']

    def get_form(self):
        form = super().get_form()
        form.fields['arrive_date'].widget = DateTimePickerInput()
        form.fields['special_request'].widget.attrs.update({'placeholder': 'MUST MATCH DRIVER INFO. PLEASE LEAVE IT BLANK IF NOT SURE'})
        return form
    
    def form_valid(self,form):
        form.instance.owner=self.request.user
        form.instance.status='OP'
        return super().form_valid(form)


#Page for owner to update currently open ride
class RideUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Rides
    template_name='rideshare/ride_form.html'
    
    fields=['destination','arrive_date','number_passenger','share','vehicle_type','special_request']
    def get_form(self):
        form = super().get_form()
        form.fields['share'].widget = forms.HiddenInput()
        return form
    def form_valid(self,form):
        form.instance.owner=self.request.user
        form.instance.has_sharer=='N'
        # form.instance.sharer__isnull==True
        form.instance.status=='OP'
        return super().form_valid(form)
    
    def test_func(self):
        ride=self.get_object()
        if self.request.user==ride.owner and ride.status=='OP' and ride.has_sharer=='N' :
            return True
        return False

#page for owner to delete open ride
class RideDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Rides
    template_name='rideshare/ride_confirm_delete.html'
    success_url=reverse_lazy('rideshare:home')
    def form_valid(self, form):
        ride=self.get_object()
        ride.status='CA'
        ride.send_email()
        return super().form_valid(form)

    def test_func(self):
        ride=self.get_object()
        if self.request.user==ride.owner and ride.status=='OP':
            return True
        return False

#Home Page for ride sharer, a button to join new ride and a list of all the share open ride
@login_required(login_url="rideshare:login")
def sharerhome(request):
    content={
        'rides':Rides.objects.filter(sharer=request.user,status='OP')
    }
    return render(request,"rideshare/sharehome.html",content)


#Page for Sharer to search for rides 
class SharerCreatelView(LoginRequiredMixin,CreateView):
    model=sharer_search
    template_name='rideshare/share_search.html'
    
    fields=['destination','arrive_date_early','arrive_date_late','number_passenger']
    def get_form(self):
        form = super().get_form()
        form.fields['arrive_date_early'].widget = DateTimePickerInput()
        form.fields['arrive_date_late'].widget = DateTimePickerInput()
        return form
    
    def form_valid(self,form):
        form.instance.sharer=self.request.user
        return super().form_valid(form)

@login_required(login_url="rideshare:login")
def sharersearchlist(request):
    share = request.user.sharer_search_set.last()
    content={
        'rides':Rides.objects.filter(
            destination=share.destination,
            number_passenger__lt=6-share.number_passenger,
            arrive_date__range=(share.arrive_date_early,share.arrive_date_late),
            status='OP').exclude(owner=request.user)
    }
    return render(request,"rideshare/share_list.html",content)

#page for sharer to join the ride
@login_required(login_url="rideshare:login")
def sharerjoin(request,pk):
    share = sharer_search.objects.filter(sharer=request.user.id).last()
    ride=Rides.objects.filter(pk=pk).first()
    ride.number_passenger=ride.number_passenger+share.number_passenger
    ride.sharer.add(share.sharer)
    ride.has_sharer='Y'
    ride.save()
    share.join_ride=pk
    share.save()
    content={
        'rides':Rides.objects.filter(pk=pk,status='OP').first()
    }
    return render(request,"rideshare/share_join_detail.html",content)

#page for sharer to view the details
@login_required(login_url="rideshare:login")
def sharedetail(request,pk):
    the_share = sharer_search.objects.filter(join_ride=pk).last()
    the_ride=Rides.objects.filter(pk=pk).first()
    return render(request,"rideshare/share_detail.html",{
        'ride':the_ride,
        'share':the_share,
        })


#page for sharer to update number of sharer passenger
@login_required(login_url="rideshare:login")
def shareupdate(request,pk):
    # user=request.user
    # sharer_search=user.
    # the_share = sharer_search.objects.filter(pk=pk).last()
    the_share=get_object_or_404(sharer_search,pk=pk)
    the_ride=Rides.objects.filter(pk=the_share.join_ride).first()
    the_num=the_share.number_passenger
    success_url = reverse_lazy('rideshare:sharer-list')
    if request.method == 'GET':
        form = SharerUpdateForm(instance=the_share)
        form.fields['destination'].widget = forms.HiddenInput()
        # success_url = reverse_lazy('rideshare:sharer-list')
    else:
        # Post method.
        form = SharerUpdateForm(request.POST, instance=the_share)
        form.fields['destination'].widget = forms.HiddenInput()
        
        if form.is_valid():
            form.save()
            the_ride.number_passenger=the_ride.number_passenger+form.instance.number_passenger-the_num
            the_ride.save()
        else:
            messages.error(request, 'Invalid arguments supplied.')   
    
    return render(request,"rideshare/share_update.html",{
        'form':form,
        })    



#page for shsare to cancel join sharer
@login_required(login_url="rideshare:login")
def sharercancel(request,pk):
    share = sharer_search.objects.filter(pk=pk).last()
    ride=Rides.objects.filter(pk=share.join_ride).first()
    ride.number_passenger=ride.number_passenger-share.number_passenger
    ride.sharer.remove(share.sharer)
    # if ride.sharer.all()==None:
    #     ride.has_sharer='N'
    ride.save()
    # print(ride.sharer.all())
    # if ride.sharer.all()==None:
    if ride.sharer.all().count()==0:
        ride.has_sharer='N'
    ride.save()
    share.join_ride=0
    share.save()
    content={
        'rides':Rides.objects.filter(sharer=request.user,status='OP')
    }
    return render(request,"rideshare/sharehome.html",content)

# Home page for registered user
@login_required(login_url="rideshare:login")
def home(request):
    current_user = request.user
    return render(request, "rideshare/home.html", {"current_user": current_user, "hasDriverAccount": hasattr(current_user, "driver") })

# Page to register as a driver
class DriverRegisterView(LoginRequiredMixin, CreateView):
    model = Driver
    fields = ['name', 'vehicle_type', 'license_number', 'capacity', 'special_vehicle_info']

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
# Home page for registered driver
@login_required(login_url="rideshare:login")
def driverhome(request):
    return render(request, "rideshare/driverhome.html", {"driver": request.user.driver});

# Page to show driver details, update any info and delete driver account
class DriverDetailView(LoginRequiredMixin, DetailView):
    model = Driver
    template_name ='rideshare/driverinfo.html'


# Page for registered driver to look for available rides
@login_required(login_url="rideshare:login")
def driverhistory(request):
    content={
        'rides':Rides.objects.filter(driver = request.user.driver).order_by("-arrive_date")
    }
    return render(request,"rideshare/driverhistory.html",content)
    

#Page for driver to update driver information
class DriverUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Driver
    template_name='rideshare/driverupdate.html'
    fields = ['name', 'vehicle_type', 'license_number', 'capacity', 'special_vehicle_info']
    
    def test_func(self):
        driver = self.get_object()
        if self.request.user == driver.user:
            return True
        return False

# Page for driver to delete driver account
class DriverDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Driver
    template_name = 'rideshare/driver_confirm_delete.html'
    success_url = reverse_lazy('rideshare:home')
    def test_func(self):
        driver = self.get_object()
        if self.request.user == driver.user:
            return True
        return False

# Checking if the user is a registered driver
def driver_check(user):
    return hasattr(user, "driver")

# Page for registered driver to search for open ride requests
@login_required(login_url="rideshare:login")
@user_passes_test(driver_check, login_url="rideshare:registerdriver")
def riderequests(request):
    content={
        'rides':Rides.objects.filter(status='OP')\
        .exclude(owner=request.user)\
        .filter(number_passenger__lt = request.user.driver.capacity)\
        .filter(vehicle_type = request.user.driver.vehicle_type)\
        .filter(Q(special_request = '') | Q(special_request__isnull=True) \
                | Q(special_request__isnull=False, special_request = request.user.driver.special_vehicle_info))
    }
    return render(request,"rideshare/riderequests.html",content)

# Page for driver to accept an open ride request 
class ClaimRideView(LoginRequiredMixin, UpdateView):
    model = Rides
    template_name='rideshare/claim_ride.html'
    success_url = reverse_lazy('rideshare:driverhome')
    fields = ['destination','arrive_date','number_passenger','share','vehicle_type','special_request', 'status']

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.status = 'CF'
        form.instance.driver = self.request.user.driver
        form.instance.send_email()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
         form = super().get_form( form_class)
         form.fields['destination'].widget = forms.HiddenInput()
         form.fields['arrive_date'].widget = forms.HiddenInput()
         form.fields['number_passenger'].widget = forms.HiddenInput()
         form.fields['share'].widget = forms.HiddenInput()
         form.fields['vehicle_type'].widget = forms.HiddenInput()
         form.fields['special_request'].widget = forms.HiddenInput()
         form.fields[ 'status'].widget = forms.HiddenInput()
         return form

# Page for driver to view ride details and complete any confirmed ride 
class CompleteRideView(LoginRequiredMixin, UpdateView):
    model = Rides
    template_name='rideshare/complete_ride.html'
    success_url = reverse_lazy('rideshare:driverhome')
    fields = ['destination','arrive_date','number_passenger','share','vehicle_type','special_request', 'status']

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.instance.status = 'CL'
        form.instance.send_email()
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
         form = super().get_form( form_class)
         form.fields['destination'].widget = forms.HiddenInput()
         form.fields['arrive_date'].widget = forms.HiddenInput()
         form.fields['number_passenger'].widget = forms.HiddenInput()
         form.fields['share'].widget = forms.HiddenInput()
         form.fields['vehicle_type'].widget = forms.HiddenInput()
         form.fields['special_request'].widget = forms.HiddenInput()
         form.fields[ 'status'].widget = forms.HiddenInput()
         return form
