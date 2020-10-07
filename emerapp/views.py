from emerapp.models import Patient
from django.shortcuts import render, redirect
from emerapp.forms import PatientForm
#from geoposition.fields import GeopositionField

import random
from datetime import datetime
from datetime import timedelta


def response(request):
    form = PatientForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            patient = form.save(commit=False)
            patient.save()
        return redirect('results.html')
    else:
        form = PatientForm()
    return render(request, 'emerapp/response.html', {'form': form})


def results(request):
    h1 = None
    h2 = None
    h3 = None
    n1 = None
    n2 = None
    n3 = None
    
    h = ['가톨릭대학교의정부성모병원','경기도의료원의정부병원','의료법인영동의료재단의정부백병원','추병원']
    i = random.choice([1,2,3]) #불가능한 병원의 개수
    a = random.sample(range(1,4),4-i) #병원 순서 순위
    p1 = random.sample(range(0,1),1) #시간 더할 함수
    p2 = random.sample(range(20,59),4-i)
    p1.sort()
    p2.sort()
    #n.hour+n.minute
    n = datetime.now()
    #timedelta(hours = %d) %1
    #timedelta(minutes = %d) %3 
    if i==1:
        n1 = n+timedelta(hours = 0)+timedelta(minutes = p2[0])
        n2 = n+timedelta(hours = p1[0])+timedelta(minutes = p2[1])
        n3 = n+timedelta(hours = p1[0])+timedelta(minutes = p2[2])
        h1 = h[a[0]%4]
        h2 = h[a[1]%4]
        h3 = h[a[2]%4]
    elif i==2:
        n1 = n+timedelta(hours = 0)+timedelta(minutes = p2[0])
        n2 = n+timedelta(hours = p1[0])+timedelta(minutes = p2[1])
        h1 = h[a[0]%4]
        h2 = h[a[1]%4]
    else:
        n1 = n+timedelta(hours = p1[0])+timedelta(minutes = p2[0])
        h1 = h[a[0]%4]
        
    context = {
        'h1': h1,
        'h2': h2,
        'h3': h3,
        'n1': n1,
        'n2': n2,
        'n3': n3,
    }
    return render(request, 'emerapp/results.html', context)