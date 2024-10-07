from django.http import HttpResponseRedirect
from django.shortcuts import render


from . import forms
from .models import MilkData, MilkView, Months

# Create your views here.


# Home page of application
def index(request):
    month_form = forms.MonthsForm()
    milk_data = MilkView.objects.all()
    return render(request, 'index.html', {'milk_data': milk_data, 'month_form': month_form})


# save todos here
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
            return HttpResponseRedirect('/')
        else:
            print(milk_form.errors)
    return render(request, 'milk.html', {'milk_form': milk_form, 'data': all_milk, 'milk_data':milk_view})


# update todos 
def update_milk_data(request, pk):
    pass
    

# delete todos
def delete_milk_data(request, pk):
    delete_milk = MilkData.objects.get(id=pk)
    print(delete_milk)
    delete_milk.delete()
    return HttpResponseRedirect('/')


def calculate_price(request):
    milk_qty = MilkData.objects.all()
    milk_data = MilkView.objects.all()
    total_price = 0
    total_qty = 0
    for milk in milk_data:
        total_price += milk.price
    for qty in milk_qty:
        total_qty += qty.qty
    
    return render(request, 'index.html', {'milk_data':milk_data,'total_price': total_price, 'total_qty': total_qty})

