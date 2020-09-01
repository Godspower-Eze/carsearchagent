from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from .tasks import data_sender, searched_value_sender


# Create your views here.
def index(request):
    data_sender.delay()
    return render(request, 'local/index.html')


def search(request):
    if request.method == 'POST':
        vehicle_type = request.POST.get('vehicle-type')
        if vehicle_type == 'VEHICLE TYPE':
            vehicle_type = None
        print(vehicle_type)
        gearing = request.POST.get('gearing')
        if gearing == 'GEARING':
            gearing = None
        print(gearing)
        fuel = request.POST.get('fuel')
        if fuel == 'FUEL':
            fuel = None
        print(fuel)
        min_price = request.POST.get('min-price')
        if min_price == 'MIN PRICE':
            min_price = None
        else:
            min_price = int(min_price)
        print(min_price)
        max_price = request.POST.get('max-price')
        if max_price == 'MAX PRICE':
            max_price = None
        else:
            max_price = int(max_price)
        print(max_price)
        year_model = request.POST.get('year-model')
        if year_model == 'YEAR MODEL':
            year_model = None
        print(year_model)
        min_mileage = request.POST.get('min-mileage')
        if min_mileage == 'MIN MILEAGE':
            min_mileage = None
        else:
            min_mileage = int(min_mileage)
        print(min_mileage)
        max_mileage = request.POST.get('max-mileage')
        if max_mileage == 'MAX MILEAGE':
            max_mileage = None
        else:
            max_mileage = int(max_mileage)
        print(max_mileage)
        searchlist = [vehicle_type, gearing, fuel, year_model]
        print(searchlist)
        mileagerange = [min_mileage, max_mileage]
        print(mileagerange)
        pricerange = [min_price, max_price]
        print(pricerange)
        searched_value_sender.delay(mileagerange, pricerange, searchlist)
    return render(request, 'local/search.html')


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cars')
    context = {
        'form': form
    }
    return render(request, 'local/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('cars')
