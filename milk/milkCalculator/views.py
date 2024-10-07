from django.http import HttpResponseRedirect
from django.shortcuts import render


from . import forms
from .models import MilkData, MilkView, Months


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.


# Home page of application
def index(request):
    month_form = forms.MonthsForm()
    milk_data = MilkView.objects.all()
    return render(request, 'index.html', {})
    # return render(request, 'index.html', {'milk_data': milk_data, 'month_form': month_form})


@login_required
def show_milk_data(request):
    return render(request, 'show_data.html', {'milk_data': MilkData.objects.all()})
    


# save todos here
@login_required
def save_milk_data(request):
    milk_form = forms.MilkForm()
    all_milk = MilkData.objects.all()
    milk_view = MilkView.objects.all()
    if request.method == 'POST':
        milk = MilkData()
        milk_form = forms.MilkForm(request.POST)
        if milk_form.is_valid():
            issue_date = milk_form.cleaned_data['issue_date']
            qty = milk_form.cleaned_data['qty']
            milk_form.save()
            return HttpResponseRedirect('/milk-form/')
            # return HttpResponseRedirect('/')
        else:
            print(milk_form.errors)
    return render(request, 'milk.html', {'milk_form': milk_form, 'data': all_milk, 'milk_data':milk_view})


# update todos 
@login_required
def update_milk_data(request, pk):
    pass
    

# delete todos
@login_required
def delete_milk_data(request, pk):
    delete_milk = MilkData.objects.get(id=pk)
    print(delete_milk)
    delete_milk.delete()
    return HttpResponseRedirect('/')


@login_required
def calculate_price(request):
    milk_form = forms.MilkForm()
    milk_qty = MilkData.objects.all()
    milk_data = MilkView.objects.all()
    total_price = 0
    total_qty = 0
    for milk in milk_data:
        total_price += milk.price
    for qty in milk_qty:
        total_qty += qty.qty

    return render(request, 'milk.html', {'milk_form': milk_form,'milk_data':milk_data,'total_price': total_price, 'total_qty': total_qty})



def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)
        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('milk_list:home'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'login.html', {})
    


def register(request):
    registered = False
    if request.method == 'POST':
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)
        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save User Form to Database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # Update with Hashed password
            user.save()
            # Now we deal with the extra info!
            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)
            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user
            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
            # Now save model
            profile.save()
            # Registration Successful!
            registered = True
        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)
    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = forms.UserForm()
        profile_form = forms.UserProfileInfoForm()
    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})



@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('milk_list:home'))