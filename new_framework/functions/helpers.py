
import re
from datetime import datetime, date, timedelta
from dateutil import rrule

def remove_pattern_from_string(string,patterns):
    regexPattern = '|'.join(map(re.escape,patterns))
    stripped_string = re.split(regexPattern,string)
    return stripped_string

def return_date_entitytweetfile(tweetfile):
    return date(int(tweetfile[-43:-39]),int(tweetfile[-39:-37]),int(tweetfile[-37:-35]))

def return_timeobj_date(sdate):
    year = str(sdate.year)
    month = str(sdate.month)
    cmonth = "0" + month if len(month) == 1 else month
    day = str(sdate.day)
    cday = "0" + day if len(day) == 1 else day
    timeobj = year + cmonth + '/' + year + cmonth + cday
    return timeobj

def return_tweetfiles_window(last_tweetfile, window_size):
    tweetfile_dt = return_date_entitytweetfile(last_tweetfile)
    first_date = tweetfile_dt - timedelta(days=window_size)
    current = first_date
    tweetfile_templates = []
    while current <= tweetfile_dt:
        timeobj = return_timeobj_date(current)
        tweetfile_templates.append(timeobj)
        current += timedelta(days=1)
    return tweetfile_templates

def return_daterange(startdate,num_days):
    return [x.date() for x in list(rrule.rrule(rrule.DAILY,count=num_days,dtstart=startdate))]
