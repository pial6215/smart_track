from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Site, Attendance
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db.models import Q, Sum, Count
import csv
from django.http import HttpResponse
from .forms import ElegantUserCreationForm
from django.contrib.auth import login

@login_required
def dashboard(request):
    active_attendance = Attendance.objects.filter(user=request.user, check_out__isnull=True).first()
    sites = Site.objects.filter(user=request.user)
    
    filter_type = request.GET.get('range', 'all')
    now = timezone.localtime(timezone.now())
    today_date = now.date()
    
    query = Q(user=request.user, check_out__isnull=False)
    
    if filter_type == 'today':
        query &= Q(check_in__date=today_date)
    elif filter_type == 'weekly':
        query &= Q(check_in__date__gte=today_date - timedelta(days=7))
    elif filter_type == 'monthly':
        query &= Q(check_in__date__gte=today_date - timedelta(days=30))
    elif filter_type == 'yearly':
        query &= Q(check_in__date__gte=today_date - timedelta(days=365))

    history = Attendance.objects.filter(query).order_by('-check_in')

  
    site_segments_raw = Attendance.objects.filter(query).values('site__name').annotate(
        total_count=Count('id'),
        total_break_sec=Sum('total_break_seconds')
    ).order_by('-total_count')

    site_segments = []
    for segment in site_segments_raw:
        break_sec = segment['total_break_sec'] or 0
        segment['total_break_min'] = round(break_sec / 60, 1)
        site_segments.append(segment)

    total_active_seconds = 0
    

    for item in history:
        if item.check_in and item.check_out:
            duration = (item.check_out - item.check_in).total_seconds()
            net_seconds = duration - item.total_break_seconds
            if net_seconds > 0:
                total_active_seconds += net_seconds

 
    if active_attendance:
     
        elapsed = (timezone.now() - active_attendance.check_in).total_seconds()
        
  
        running_break_sec = 0
        if active_attendance.break_start:
            running_break_sec = (timezone.now() - active_attendance.break_start).total_seconds()
            
        net_active_sec = elapsed - active_attendance.total_break_seconds - running_break_sec
        if net_active_sec > 0:
            total_active_seconds += net_active_sec

    total_hours = int(total_active_seconds // 3600)
    total_minutes = int((total_active_seconds % 3600) // 60)
    summary_text = f"{total_hours}h {total_minutes}m"

    context = {
        'active_record': active_attendance,
        'sites': sites,
        'history': history,
        'site_segments': site_segments,
        'summary_text': summary_text,
        'current_filter': filter_type,
    }
    return render(request, 'tracker/dashboard.html', context)

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
          
            now_time = timezone.now()
            if attendance.break_start:
                delta = now_time - attendance.break_start
                attendance.total_break_seconds += int(delta.total_seconds())
                attendance.break_start = None
            
            manual_time = request.POST.get('manual_checkout_time')
            if manual_time:
                attendance.check_out = manual_time
            else:
                attendance.check_out = now_time
            
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
def export_attendance(request):
    filter_type = request.GET.get('range', 'all')
    now = timezone.localtime(timezone.now())
    query = Q(user=request.user, check_out__isnull=False)
    
    if filter_type == 'today':
        query &= Q(check_in__date=now.date())
    elif filter_type == 'weekly':
        query &= Q(check_in__date__gte=now.date() - timedelta(days=7))

    history = Attendance.objects.filter(query).order_by('-check_in')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{filter_type}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Site', 'Date', 'Check In', 'Check Out', 'Break (Sec)', 'Duration'])

    for row in history:
        c_in = timezone.localtime(row.check_in)
        c_out = timezone.localtime(row.check_out)
        writer.writerow([
            row.site.name, 
            c_in.strftime('%Y-%m-%d'),
            c_in.strftime('%H:%M'), 
            c_out.strftime('%H:%M'), 
            row.total_break_seconds,
            row.get_duration()
        ])
    return response

from django.contrib import messages 

def signup(request):
    if request.method == 'POST':
        form = ElegantUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login to start your shift.')
            return redirect('login') 
    else:
        form = ElegantUserCreationForm() 
    return render(request, 'tracker/signup.html', {'form': form})

@login_required
def add_site(request):
    if request.method == 'POST':
        name = request.POST.get('site_name')
        if name:
            Site.objects.create(name=name, user=request.user)
    return redirect('dashboard')