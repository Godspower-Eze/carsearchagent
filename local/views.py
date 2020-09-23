from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from .tasks import data_sender, searched_value_sender
from django_celery_beat.models import PeriodicTask
from .models import SearchedValue


# Create your views here.
def index(request):
    data_sender.delay()
    return render(request, 'local/index.html')


def search(request):
    if request.method == 'POST':
        searchlistmain = []
        vehicle_type = request.POST.get('vehicle-type')
        if vehicle_type == 'VEHICLE TYPE':
            vehicle_type = None
        gearing = request.POST.get('gearing')
        if gearing == 'GEARING':
            gearing = None
        fuel = request.POST.get('fuel')
        if fuel == 'FUEL':
            fuel = None
        min_price = request.POST.get('min-price')
        if min_price == 'MIN PRICE':
            min_price = None
        else:
            min_price = int(min_price)
        max_price = request.POST.get('max-price')
        if max_price == 'MAX PRICE':
            max_price = None
        else:
            max_price = int(max_price)
        year_model_min = request.POST.get('year-model-min')
        print(year_model_min)
        if year_model_min == 'YEAR MODEL(MIN)':
            year_model_min = None
        print(year_model_min)
        year_model_max = request.POST.get('year-model-max')
        if year_model_max == 'YEAR MODEL(MAX)':
            year_model_max = None
        print(year_model_max)
        min_mileage = request.POST.get('min-mileage')
        if min_mileage == 'MIN MILEAGE':
            min_mileage = None
        else:
            min_mileage = int(min_mileage)
        max_mileage = request.POST.get('max-mileage')
        if max_mileage == 'MAX MILEAGE':
            max_mileage = None
        else:
            max_mileage = int(max_mileage)
        car = request.POST.get('id_make')
        if car == 'MAKE (Merkki)':
            car = None
        print(car)
        carmodel = request.POST.get('car-model-type')
        # print(carmodel)
        if carmodel == 'CAR MODEL':
            carmodel = None
        print(carmodel)
        airconditioner = request.POST.get('air-conditioning')
        servicebook = request.POST.get('service-book')
        cruisecontrol = request.POST.get('cruise-control')
        isofixreadiness = request.POST.get('isofix-readiness')
        leatherupholstery = request.POST.get('leather-upholstery')
        motorheater = request.POST.get('motor-heater')
        internalplug = request.POST.get('internal-plug')
        twotires = request.POST.get('two-tires')
        parkingsensors = request.POST.get('parking-sensors')
        xenonheadlights = request.POST.get('xenon-headlights')
        ledheadlights = request.POST.get('led-headlights')
        webastoeber = request.POST.get('webasto-eber')
        towbar = request.POST.get('towbar')
        metalliccolor = request.POST.get('metallic-color')
        year_model = [year_model_min, year_model_max]
        searchlist = [vehicle_type, gearing, car, carmodel, fuel, airconditioner, servicebook, cruisecontrol,
                      isofixreadiness, leatherupholstery, motorheater, internalplug, twotires, parkingsensors,
                      xenonheadlights, ledheadlights, webastoeber, towbar, metalliccolor]
        print(len(searchlist))
        for i in searchlist:
            if i != None:
                searchlistmain.append(i)
        print(searchlistmain)
        mileagerange = [min_mileage, max_mileage]
        pricerange = [min_price, max_price]
        searched_value_sender.delay(mileagerange, pricerange, searchlist, year_model)
        searched = SearchedValue(searchlist=searchlistmain, mileagerange=mileagerange, pricerange=pricerange,
                                 yearmodel=year_model)
        searched.save()
        searching_values = SearchedValue.objects.last()
        deletedvalue = SearchedValue.objects.get(id=searching_values.id - 1)
        deletedvalue.delete()
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
