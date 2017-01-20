
import re
import datetime

def remove_pattern_from_string(string,patterns):
    regexPattern = '|'.join(map(re.escape,patterns))
    stripped_string = re.split(regexPattern,string)
    return stripped_string

def return_tweetfiles_window(last_tweetfile, window_size):
    tweetfile_dt = datetime.datetime(int(last_tweetfile[-43:-39]),int(last_tweetfile[-39:-37]),int(last_tweetfile[-37:-35]),0,0,0)
    first_date = tweetfile_dt - datetime.timedelta(days=window_size)
    current = first_date
    tweetfile_templates = []
    while current <= tweetfile_dt:
        year = str(current.year)
        month = str(current.month)
        cmonth = "0" + month if len(month) == 1 else month
        day = str(current.day)
        cday = "0" + day if len(day) == 1 else day
        timeobj = year + cmonth + '/' + year + cmonth + cday
        tweetfile_templates.append(timeobj)
        current += datetime.timedelta(days=1)
    return tweetfile_templates
