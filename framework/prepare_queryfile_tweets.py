
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
date_queryterms = defaultdict(list)
begin = datetime.date(2010, 12, 12)
end = datetime.date(2015, 10, 31)

with open(sys.argv[1], 'r', encoding = 'utf-8') as eventfile:
    events = eventfile.readlines()

for event in events:
    tokens = event.strip().split('\t')
    date = filedate2datetime(tokens[0])
    for term in tokens[2].split('_'):
        if len(term) > 1:
            term_date.append([term, date])

for td in term_date:
    term = term_date[0]
    date = term_date[1]
    window_before = date - datetime.timedelta(days = 30)
    window_before = begin if window_before < begin
    window_after = date + datetime.timedelta(days = 30)
    window_after = end if window_after > end
    date_range = [window_before + datetime.timedelta(days = x) for x in range(0, (window_after - window_before).days)]
    for d in date_range:
        date_queryterms[d].append(term)

with open(sys.argv[2], 'w', encoding = 'utf-8') as out:
    for date in sorted(date_queryterms.keys()):
        files = datetime2twiqsfiles(date)
        for f in files:
            out.write(f + ', '.join(date_queryterms[date]) + '\n')

