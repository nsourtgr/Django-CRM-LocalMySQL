from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Record

def export_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Records"

    # Header
    ws.append([
        "First Name","Last Name","Email","Phone",
        "Address","City","State","Zipcode","Created"
    ])

    records = Record.objects.all()

    for r in records:
        ws.append([
            r.first_name,
            r.last_name,
            r.email,
            r.phone,
            r.address,
            r.city,
            r.state,
            r.zipcode,
            r.created_at.strftime("%d-%m-%Y %H:%M")
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=crm_records.xlsx"

    wb.save(response)
    return response

def home(request):
    if request.user.is_authenticated:
        records = Record.objects.all()
    else:
        records = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('home')
    
    return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registered successfully!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Login required")
        return redirect('home')
    record = Record.objects.get(id=pk)
    return render(request, 'record.html', {'customer_record': record})

def add_record(request):
    if not request.user.is_authenticated:
        messages.error(request, "Login required")
        return redirect('home')
    form = AddRecordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Record added!")
        return redirect('home')
    return render(request, 'add_record.html', {'form': form})

def update_record(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Login required")
        return redirect('home')
    record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=record)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Record updated!")
        return redirect('home')
    return render(request, 'update_record.html', {'form': form})

def delete_record(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "Login required")
        return redirect('home')
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Record deleted!")
    return redirect('home')

def record_search_ajax(request):
    q = request.GET.get('q', '')
    records = Record.objects.filter(
        models.Q(first_name__icontains=q) |
        models.Q(last_name__icontains=q) |
        models.Q(email__icontains=q) |
        models.Q(phone__icontains=q) |
        models.Q(address__icontains=q) |
        models.Q(city__icontains=q) |
        models.Q(state__icontains=q) |
        models.Q(zipcode__icontains=q)
    )
    data = {
        "records": [
            {
                "first_name": r.first_name,
                "last_name": r.last_name,
                "email": r.email,
                "phone": r.phone,
                "address": r.address,
                "city": r.city,
                "state": r.state,
                "zipcode": r.zipcode,
                "id": r.id,
                "created_at": r.created_at.astimezone().strftime("%d/%m/%Y %H:%M:%S")
            } for r in records
        ]
    }
    return JsonResponse(data)
