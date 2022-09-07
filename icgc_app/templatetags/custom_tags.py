from django import template
from django.shortcuts import get_object_or_404
from django.utils import timezone 
import os, pytz, datetime, random 
from django.db.models import Q, Max, Min, Sum, F 

register = template.Library()
  
@register.simple_tag
def custom_date_format(date, date_only=False): 
    
    tz = pytz.timezone('Asia/Manila') 
    if date != None:     
        # Only date with date and time
        if isinstance(date, datetime.datetime): 
            date = timezone.localtime(date, tz) 
            if date_only: 
                date = date.strftime("%b. %d, %Y") 
            else:
                date = date.strftime("%b. %d, %Y, %I:%M %p")  
        elif isinstance(date, datetime.date): 
            date = date.strftime("%b. %d, %Y") 
                
    return date

 
@register.filter
def custom_time_format(time):
    if time != None:       
        time = time.strftime("%I:%M %p")   
    return time

@register.filter
def custom_date_only_format(date, args=None):
    if date != None:       
        date = date.strftime("%b. %d, %Y") 
 
        if args is not None:  
            parsed_dt = datetime.datetime.strptime(date, '%b. %d, %Y')
            date = parsed_dt.strftime(args)  

    return date
  


