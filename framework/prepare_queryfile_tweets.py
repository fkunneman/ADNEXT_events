
import sys
from collections import defaultdict
import datetime

def datetime2twiqsfiles(dt):
    year = str(dt.year)
    month = str(dt.month)
    month = '0' + month if len(month) == 1 else month
    day = str(dt.day)
    day = '0' + day if len(day) == 1 else day
    date_template = year + month + day + '-'
    files = []
    for hour in range(24):
        h = '0' + str(hour) if hour < 10 else str(hour)
        files.append(date_template + h + '.out')

    return files

def filedate2datetime(fd):
    year = int(fd[:4])
    month = int(fd[5:7])
    day = int(fd[8:])
    return datetime.date(year, month, day)

term_date = []
twiqsfile_queryterms = defaultdict(list)
begin = datetime.date(2010, 12, 12)
end = datetime.date(2015, 10, 31)

with open(sys.argv[1], 'r', encoding = 'utf-8') as eventfile:
    events = eventfile.readlines()

print(events[:10])
#for event in events:
