import datetime

SECONDS_PER_DAY = 86400
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60

def get_elapse_time(total_seconds):
   #print total_seconds
   min_value, hour_value, day_value = '', '', ''
   days = int(total_seconds / SECONDS_PER_DAY)
   hours = int((total_seconds % SECONDS_PER_DAY) / SECONDS_PER_HOUR)
   minutes = int(((total_seconds % SECONDS_PER_DAY) % SECONDS_PER_HOUR) / SECONDS_PER_MINUTE)
   if minutes == 1: 
      min_value = " minute"
   else: 
      min_value = ' minutes'
   if hours == 1: 
      hour_value = ' hour'
   else: 
      hour_value = ' hours'
   if days == 1: 
      day_value = ' day'
   else: 
      day_value = ' days' 
   if days == 0 and hours == 0 and minutes == 0:
   	return "a few seconds ago"
   if days == 0 and hours == 0:
   	return str(minutes) + min_value + " ago"
   if days == 0:
   	return str(hours) + hour_value + " and " + str(minutes) + min_value + " ago"
   return str(days) + day_value + " ago"