from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User


from . import forms
from .models import MilkData, Months, UserProfileInfo


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

# Home page of application
def index(request):
    month_form = forms.MonthsForm()
    return render(request, 'index.html', {})
    # return render(request, 'index.html', {'milk_data': milk_data, 'month_form': month_form})


@login_required
def show_milk_data(request):
    user_id = request.user.id
    # milk_data = MilkData.objects.get(pk=request.user.id)
    milk_data = MilkData.objects.all()

    return render(request, 'show_data.html', {'milk_data': milk_data})
    


# save milk data here
@login_required
def save_milk_data(request):

    user_id = request.user.id
    milk_form = forms.MilkForm()
    milk_data = MilkData.objects.filter(user_id__pk=user_id)
    if request.method == 'POST':
        milk_form = forms.MilkForm(request.POST)
        if milk_form.is_valid():
            if request.user.is_authenticated:
                total_qty = 0
                total_price = 0
                filtered_milk = MilkData.objects.filter(user_id__pk=user_id)
                for milk in filtered_milk:
                    total_qty += milk.qty
                    total_price += milk.price
                print(request.user)
                issue_date = milk_form.cleaned_data['issue_date']
                qty = milk_form.cleaned_data['qty']
                intance = MilkData(qty=qty, issue_date=issue_date, price=qty*68, total_qty=total_qty+qty,total_price=total_price+(qty*68) ,user=request.user)
                intance.save()
                # milk_form.save()
                return HttpResponseRedirect('/milk-form/')
                # return HttpResponseRedirect('/')
        else:
            print(milk_form.errors)
    return render(request, 'milk.html', {'milk_form': milk_form, 'milk_data':milk_data})


# update milk data 
@login_required
def update_milk_data(request, pk):
    milk_data = MilkData.objects.get(pk=pk)
    form = forms.MilkForm(instance=milk_data)
    if request.method == 'POST':
        existed_milk = MilkData.objects.get(pk=pk)
        issue_date = request.POST['issue_date']
        qty = request.POST['qty']
        existed_milk.issue_date = issue_date
        existed_milk.qty= qty
        existed_milk.total_price = qty * 68
        existed_milk.total_qty = existed_milk.total_qty + float(qty)
        existed_milk.save()
        return HttpResponseRedirect('/milk-form/')
    else:
         return render(request, 'update.html', {'milk_form':form})
    
    

# delete milk data
@login_required
def delete_milk_data(request, pk):
    delete_milk = MilkData.objects.get(id=pk)
    print(delete_milk)
    delete_milk.delete()
    return HttpResponseRedirect('/milk-form/')
    # return HttpResponseRedirect('/milk-form/')


@login_required
def calculate_price(request):
    user_id = request.user.id
    milk_form = forms.MilkForm()
    milk_data = MilkData.objects.filter(user_id__pk=user_id)
    total_price = 0
    total_qty = 0
    for milk in milk_data:
        total_price += milk.price
        total_qty += milk.qty
        

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
            return HttpResponse("Invalid Username or Password.")

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



@login_required
def show_profile(request, pk):
    user_data = User.objects.get(pk=pk)
    user_photo = UserProfileInfo.objects.get(user_id__pk=pk)
    return render(request, 'profile.html', {'user': user_data, 'user_photo': user_photo})