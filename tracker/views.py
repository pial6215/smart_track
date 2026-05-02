from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Site, Attendance
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db.models import Q

@login_required
def dashboard(request):
    active_attendance = Attendance.objects.filter(user=request.user, check_out__isnull=True).first()
    sites = Site.objects.all()
    
    # Filter Logic
    filter_type = request.GET.get('range', 'all')
    now = timezone.now()
    query = Q(user=request.user, check_out__isnull=False)
    
    if filter_type == 'today':
        query &= Q(check_in__date=now.date())
    elif filter_type == 'weekly':
        start_date = now.date() - timedelta(days=7)
        query &= Q(check_in__date__gte=start_date)
    elif filter_type == 'monthly':
        start_date = now.date() - timedelta(days=30)
        query &= Q(check_in__date__gte=start_date)

    history = Attendance.objects.filter(query).order_by('-check_in')

  # --- TOTAL SUMMARY CALCULATION START ---
total_active_seconds = 0
for item in history:
    if item.check_in and item.check_out:
     
        duration = (item.check_out - item.check_in).total_seconds()
        
        net_seconds = duration - item.total_break_seconds
        
        if net_seconds > 0:
            total_active_seconds += net_seconds

if total_active_seconds < 0:
    total_active_seconds = 0

total_hours = int(total_active_seconds // 3600)
total_minutes = int((total_active_seconds % 3600) // 60)
summary_text = f"{total_hours}h {total_minutes}m"
# --- TOTAL SUMMARY CALCULATION END ---
@login_required
def check_in(request):
    if request.method == 'POST':
        site_id = request.POST.get('site')
        site = get_object_or_404(Site, id=site_id)
        if not Attendance.objects.filter(user=request.user, check_out__isnull=True).exists():
            Attendance.objects.create(user=request.user, site=site)
    return redirect('dashboard')

@login_required
def check_out(request):
    if request.method == 'POST':
        attendance = Attendance.objects.filter(user=request.user, check_out__isnull=True).first()
        if attendance:
            # User jodi manual checkout time dey, sheta nibe, noile current time
            manual_time = request.POST.get('manual_checkout_time')
            if manual_time:
                attendance.check_out = manual_time
            else:
                attendance.check_out = timezone.now()
            
            # Break check
            if attendance.break_start:
                delta = attendance.check_out - attendance.break_start
                attendance.total_break_seconds += int(delta.total_seconds())
                attendance.break_start = None
            
            attendance.save()
    return redirect('dashboard')

@login_required
def toggle_break(request):
    attendance = Attendance.objects.filter(user=request.user, check_out__isnull=True).first()
    if attendance:
        if not attendance.break_start:
            attendance.break_start = timezone.now()
        else:
            delta = timezone.now() - attendance.break_start
            attendance.total_break_seconds += int(delta.total_seconds())
            attendance.break_start = None
        attendance.save()
    return redirect('dashboard')

@login_required
def manual_entry(request):
    if request.method == 'POST':
        site_id = request.POST.get('site')
        check_in_time = request.POST.get('check_in')
        check_out_time = request.POST.get('check_out')
        break_mins = int(request.POST.get('break_minutes') or 0)
        
        site = get_object_or_404(Site, id=site_id)
        
        Attendance.objects.create(
            user=request.user,
            site=site,
            check_in=check_in_time,
            check_out=check_out_time,
            total_break_seconds=break_mins * 60
        )
    return redirect('dashboard')
@login_required
def add_site(request):
    if request.method == 'POST':
        name = request.POST.get('site_name')
        if name:
            Site.objects.create(name=name)
    return redirect('dashboard')
import csv
from django.http import HttpResponse

@login_required
def export_attendance(request):
    filter_type = request.GET.get('range', 'all')
    now = timezone.now()
    query = Q(user=request.user, check_out__isnull=False)
    
    if filter_type == 'today':
        query &= Q(check_in__date=now.date())
    elif filter_type == 'weekly':
        query &= Q(check_in__date__gte=now.date() - timedelta(days=7))
    elif filter_type == 'monthly':
        query &= Q(check_in__date__gte=now.date() - timedelta(days=30))

    history = Attendance.objects.filter(query).order_by('-check_in')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{filter_type}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Site', 'Date', 'Check In', 'Check Out', 'Break (Sec)', 'Duration'])

    for row in history:
        writer.writerow([
            row.site.name, 
            row.check_in.strftime('%Y-%m-%d'),
            row.check_in.strftime('%H:%M'), 
            row.check_out.strftime('%H:%M'), 
            row.total_break_seconds,
            row.get_duration()
        ])

    return response
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import ElegantUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = ElegantUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = ElegantUserCreationForm() 
    return render(request, 'tracker/signup.html', {'form': form})