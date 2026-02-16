from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.utils import timezone

from openpyxl import Workbook

from .forms import SignUpForm, AddRecordForm
from .models import Record


# ===================== EXPORT EXCEL =====================

def export_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Records"

    ws.append([
        "First Name", "Last Name", "Email", "Phone", "Work Phone",
        "Address", "City", "State", "Zipcode", "Created"
    ])

    records = Record.objects.all().order_by("-created_at")

    for r in records:
        ws.append([
            r.first_name,
            r.last_name,
            r.email,
            r.phone,
            r.work_phone,
            r.address,
            r.city,
            r.state,
            r.zipcode,
            timezone.localtime(r.created_at).strftime("%d-%m-%Y %H:%M")
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=crm_records.xlsx"

    wb.save(response)
    return response


# ===================== HOME / LOGIN =====================

def home(request):
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

    return render(request, 'home.html')


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


# ===================== CRUD =====================

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


# ===================== AJAX SEARCH (DataTables) =====================

def record_search_ajax(request):
    q = request.GET.get('q', '')

    records = Record.objects.filter(
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q) |
        Q(email__icontains=q) |
        Q(phone__icontains=q) |
        Q(work_phone__icontains=q) |
        Q(address__icontains=q) |
        Q(city__icontains=q) |
        Q(state__icontains=q) |
        Q(zipcode__icontains=q)
    ).order_by('-created_at')

    data = {
        "data": [
            {
                "first_name": r.first_name,
                "last_name": r.last_name,
                "email": r.email,
                "phone": r.phone,
                "work_phone": r.work_phone,   # must match DataTables column
                "address": r.address,
                "city": r.city,
                "state": r.state,
                "zipcode": r.zipcode,
                "id": r.id,
                "created_at": timezone.localtime(r.created_at).strftime("%d/%m/%Y %H:%M")
            }
            for r in records
        ]
    }

    return JsonResponse(data)