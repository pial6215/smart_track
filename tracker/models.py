from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Site(models.Model):
    # ১. User-এর সাথে সম্পর্ক তৈরি করা হয়েছে যাতে একজনের সাইট অন্যজন না দেখে
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(null=True, blank=True)
    
    # Break logic fields
    break_start = models.DateTimeField(null=True, blank=True)
    total_break_seconds = models.IntegerField(default=0)

    def get_duration(self):
        """Kajer prokrito somoy (Net Duration) calculate kore"""
        if self.check_in and self.check_out:
            total_seconds = int((self.check_out - self.check_in).total_seconds())
            active_seconds = total_seconds - self.total_break_seconds
            
            if active_seconds < 0: 
                active_seconds = 0
            
            hours = active_seconds // 3600
            minutes = (active_seconds % 3600) // 60
            
            return f"{hours}h {minutes}m"
        return "N/A"

    def get_break_minutes(self):
        """Break seconds ke minute-e convert kore"""
        if self.total_break_seconds > 0:
            minutes = self.total_break_seconds // 60
            if minutes == 0 and self.total_break_seconds > 0:
                return "1"
            return f"{minutes}"
        return "0"

    def __str__(self):
        date_str = self.check_in.strftime('%d %b %Y')
        return f"{self.user.username} at {self.site.name} ({date_str})"