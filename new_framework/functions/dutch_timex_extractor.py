
import re
import datetime

import time_functions

class Dutch_timex_extractor:

    def __init__(self, tweet_text, tweet_date):

        self.tweet_text = tweet_text
        self.tweet_date = tweet_date

        self.refdates = []

        self.number_dict = {
            'een'               : 1,
            'twee'              : 2,
            'drie'              : 3,
            'vier'              : 4,
            'vijf'              : 5,
            'zes'               : 6,
            'zeven'             : 7,
            'acht'              : 8,
            'negen'             : 9,
            'tien'              : 10,
            'elf'               : 11,
            'twaalf'            : 12,
            'dertien'           : 13,
            'veertien'          : 14,
            'vijftien'          : 15,
            'zestien'           : 16,
            'zeventien'         : 17,
            'achtien'           : 18,
            'negentien'         : 19,
            'twintig'           : 20,
            'eenentwintig'      : 21,
            'tweeentwintig'     : 22,
            'drieentwintig'     : 23,
            'vierentwintig'     : 24,
            'vijfentwintig'     : 25,
            'zesentwintig'      : 26,
            'zevenentwintig'    : 27,
            'achtentwintig'     : 28,
            'negenentwintig'    : 29,
            'dertig'            : 30,
            'eenendertig'       : 31
            }
        self.numbers = self.number_dict.keys()

        self.month_dict = {
            'jan' : 1, 'januari'    : 1,
            'feb' : 2, 'februari'   : 2,
            'mrt' : 3, 'maart'      : 3,
            'apr' : 4, 'april'      : 4,
            'mei' : 5, 
            'jun' : 6, 'juni'       : 6,
            'jul' : 7, 'juli'       : 7, 
            'aug' : 8, 'augustus'   : 8,
            'sep' : 9, 'september'  : 9,
            'okt' : 10, 'oktober'   : 10,
            'nov' : 11, 'november'  : 11,
            'dec' : 12, 'december'  : 12
            }
        self.months = self.month_dict.keys()
        
        self.timeunit_dict = {
            'dagen' : 1, 'daagjes' : 1, 'dag' : 1, 'dagje' : 1, 
            'nachten' : 1, 'nachtjes' : 1, 'nacht' : 1, 'nachtje' : 1, 
            'weken' : 7, 'weekjes' : 7, 'week' : 7, 'weekje' : 7,
            'maanden' : 30, 'maandjes' : 30, 'maand' : 30, 'maandje' : 30}
        self.timeunits = self.timeunit_dict.keys()

        self.weekdays = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']

        self.nums_re = (r'(\d+|een|twee|drie|vier|vijf|zes|zeven|acht|negen|tien|elf|twaalf|dertien|veertien|'
            r'vijftien|zestien|zeventien|achtien|negentien|twintig|eenentwintig|tweeentwintig|'
            r'drieentwintig|vierentwintig|vijfentwintig|zesentwintig|zevenentwintig|achtentwintig|'
            r'negenentwintig|dertig|eenendertig)')
        self.months_re = (r'(jan|januari|feb|februari|mrt|maart|apr|april|mei|jun|juni|jul|juli|aug|augustus|'
            r'sep|september|okt|oktober|nov|november|dec|december)')
        self.timeunits_re = (r'(dagen|daagjes|dag|dagje|nachten|nachtjes|nacht|nachtje|weken|weekjes|week|'
            r'weekje|maanden|maandjes|maand|maandje)')

    def extract_refdates(self, skip_date=False, skip_month=False, skip_timeunit=False, skip_day=False):
        # perform chosen information extraction
        if not skip_date:
            try:
                self.extract_date()
            except OverflowError:
                print('overflow',self.tweet_text.encode('utf-8'))
        if not skip_month:
            try:
                self.extract_month()
            except OverflowError:
                print('dateoverflow',self.tweet_text.encode('utf-8'))
        if not skip_timeunit:
            try:
                self.extract_timeunit()
            except OverflowError:
                print('overflow',self.tweet_text.encode('utf-8'))
        if not skip_day:
            try:
                self.extract_day()
            except IndexError:
                print('Index error',self.tweet_text.encode('utf-8'))                

    def return_refdates(self):
        # clean up, sort and return reference dates 
        if len(self.refdates) > 0:
            unique_refdates = list(set(self.refdates))
            sorted_refdates = sorted(unique_refdates)
            return sorted_refdates
        else:
            return False 

    def match_timex(self, list_patterns):
        #return re.findall('|'.join(list_patterns), self.tweet_text)
        matchings = [re.findall(lp,self.tweet_text) for lp in list_patterns]
        matches = sum([[s for s in m if len(s) > 0] for m in matchings],[])
        matches = matches if len(matches) > 0 else False
        return matches

    def match2timestring(self, match, joinstr):
        timestring = joinstr.join([x for x in match if x.strip() != ''])
        return timestring

    def filter_future_refdates(self):
        future_refdates = [refdate for refdate in self.refdates if refdate[1] > self.tweet_date] 
        self.refdates = future_refdates

    def extract_date(self):

        list_patterns_date = (
            r'(\b|^)(\d{2}-\d{2}-\d{2,4})(\b|$)',
            r'(\b|^)(\d{4}-\d{2}-\d{2})(\b|$)',
            r'(\b|^)(\d{2}/\d{2})(/\d{2,4})?(\b|$)',
            r'(\b|^)(\d{4}/\d{2}/\d{2})(\b|$)'
        )

        matches = self.match_timex(list_patterns_date)      
        if matches:
            for match in matches:
                datestring = self.match2timestring(match,'')
                try:
                    refdate = time_functions.return_date(datestring)
                    if refdate:
                        self.refdates.append((datestring,refdate))
                except ValueError: # given datestring is inexistable
                    continue

    def extract_month(self):

        list_pattern_month = r'(\b|^)' + (self.nums_re) + ' ' + (self.months_re) + r'( |$)' + r'(\d{4})?'

        matches = self.match_timex([list_pattern_month])
        if matches:
            for match in matches:
                timestring = self.match2timestring(match,' ')
                try:
                    day = int(match[1])
                except ValueError: # day is in written form
                    day = self.number_dict[match[1]]
                month = self.month_dict[match[2]]
                if match[-1] != '': # year information is included
                    year = int(match[4])
                else:
                    if month >= self.tweet_date.month:
                        year = self.tweet_date.year
                    else:
                        year = self.tweet_date.year+1
                try:
                    refdate = datetime.datetime(year,month,day,0,0,0)
                except ValueError: # given date is inexistent
                    continue
                self.refdates.append((timestring,refdate))

    def extract_timeunit(self):
        list_patterns_timeunits = ([r'(over|nog) (minimaal |maximaal |tenminste |bijna |ongeveer |maar |slechts |pakweg |ruim |krap |(maar )?een kleine |(maar )?iets (meer|minder) dan )?' + (self.nums_re) + ' ' + (self.timeunits_re) + r'($| )', (self.nums_re) + ' ' + (self.timeunits_re) + r'( slapen)? tot', r'met( nog)? (minimaal |maximaal |tenminste |bijna |ongeveer |maar |slechts |pakweg |ruim |krap |(maar )?een kleine |(maar )?iets (meer|minder) dan )?' + (self.nums_re) + ' ' + (self.timeunits_re) + r'( nog)? te gaan'])

        matches = self.match_timex(list_patterns_timeunits)
        if matches:
            for match in matches:
                timestring = self.match2timestring(match,' ')
                num = [x for x in match if x in self.numbers or re.match('\d', x)][0]
                if num in self.number_dict.keys():
                    num_digit = self.number_dict[num]
                else:
                    num_digit = int(num)
                timeunit = [x for x in match if x in self.timeunits][0]
                days = num_digit * self.timeunit_dict[timeunit]
                refdate = self.tweet_date + datetime.timedelta(days = days)
                self.refdates.append((timestring, refdate))

    def extract_day(self):

        list_patterns_days = ([r'(morgen|overmorgen)(avond|nacht|ochtend|middag)?', r'(volgende week|komende|aankomende|deze) (maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag)(avond|nacht|ochtend|middag)?'])
 
        matches = self.match_timex(list_patterns_days)
        if matches:
            tweet_weekday = self.tweet_date.weekday()
            for match in matches:
                timestring = self.match2timestring(match,' ')
                if 'morgen' in match:
                    days_ahead = 1
                elif 'overmorgen' in match:
                    days_ahead = 2
                else: # weekdays 
                    tweet_weekday = self.tweet_date.weekday()
                    match_weekday = [self.weekdays.index(field) for field in match if field in self.weekdays][0]
                    if 'volgende week' in match:
                        bonus = 7
                    else:
                        bonus = 0
                    if tweet_weekday <= match_weekday:
                        days_ahead = match_weekday - tweet_weekday + bonus
                    else:
                        days_ahead = match_weekday + (7-tweet_weekday) + bonus
                refdate = self.tweet_date + datetime.timedelta(days = days_ahead)
                self.refdates.append((timestring, refdate))
