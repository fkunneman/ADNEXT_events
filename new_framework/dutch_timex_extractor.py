
import re

import time_functions

class Dutch_timex_extractor:

    def __init__(self, tweet_text, tweet_date):

        self.tweet_text = tweet_text
        self.tweet_date = tweet_date

        self.number_dict = {
            'een' : 1,
            'twee' : 2,
            'drie' : 3,
            'vier' : 4,
            'vijf' : 5,
            'zes' : 6,
            'zeven' : 7,
            'acht' : 8,
            'negen' : 9,
            'tien' : 10,
            'elf' : 11,
            'twaalf' : 12,
            'dertien' : 13,
            'veertien' : 14,
            'vijftien' : 15,
            'zestien' : 16,
            'zeventien' : 17,
            'achtien' : 18,
            'negentien' : 19,
            'twintig' : 20,
            'eenentwintig' : 21,
            'tweeentwintig' : 22,
            'drieentwintig' : 23,
            'vierentwintig' : 24,
            'vijfentwintig' : 25,
            'zesentwintig' : 26,
            'zevenentwintig' : 27,
            'achtentwintig' : 28,
            'negenentwintig' : 29,
            'dertig' : 30,
            'eenendertig' : 31
            }

        self.month_dict = {
            'jan' : 1, 'januari' : 1,
            'feb' : 2, 'februari' : 2,
            'mrt' : 3, 'maart' : 3,
            'apr' : 4, 'april' : 4,
            'mei' : 5, 
            'jun' : 6, 'juni' : 6,
            'jul' : 7, 'juli' : 7, 
            'aug' : 8, 'augustus' : 8,
            'sep' : 9, 'september' : 9,
            'okt' : 10, 'oktober' : 10,
            'nov' : 11, 'november' : 11,
            'dec' : 12, 'december' : 12
            }
        
        self.timeunit_dict = {
            'dagen' : 1, 'daagjes' : 1, 'dag' : 1, 'dagje' : 1, 
            'nachten' : 1, 'nachtjes' : 1, 'nacht' : 1, 'nachtje' : 1, 
            'weken' : 7, 'weekjes' : 7, 'week' : 7, 'weekje' : 7,
            'maanden' : 30, 'maandjes' : 30, 'maand' : 30, 'maandje' : 30}

        self.weekdays = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']
        self.specific_days = ['overmorgen', 'morgen']

        self.nums = (r'(\d+|een|twee|drie|vier|vijf|zes|zeven|acht|negen|tien|elf|twaalf|dertien|veertien|'
            r'vijftien|zestien|zeventien|achtien|negentien|twintig|eenentwintig|tweeentwintig|'
            r'drieentwintig|vierentwintig|vijfentwintig|zesentwintig|zevenentwintig|achtentwintig|'
            r'negenentwintig|dertig|eenendertig)')
        self.months = (r'(jan|januari|feb|februari|mrt|maart|apr|april|mei|jun|juni|jul|juli|aug|augustus|'
            'sep|september|okt|oktober|nov|november|dec|december)')
        self.timeunits = (r'(dagen|daagjes|dag|dagje|nachten|nachtjes|nacht|nachtje|weken|weekjes|week|'
            'weekje|maanden|maandjes|maand|maandje)')



        self.list_patterns_month = ([r'(\b|^)' + (self.nums) + ' ' + (self.months) + r'( |$)' + r'(\d{4})?'])
            

            
        self.list_patterns_weekdays = ([r'(volgende week|komende|aankomende|deze) (maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag)'
            r' ?(avond|nacht|ochtend|middag)?', r'(overmorgen) ?(avond|nacht|ochtend|middag)?'])

        # date_eu = re.compile(r'(\d{1,2})-(\d{1,2})-?(\d{2,4})?')
        # date_eu2 = re.compile(r'(\d{1,4})-(\d{1,2})-?(\d{1,4})?')
        # date_vs = re.compile(r'(\d{1,4})/(\d{1,2})/(\d{1,4})')
        # date_vs2 = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{2,4})')
        # date_vs3 = re.compile(r'(\d{1,2})/(\d{1,2})')
        ns = self.number_dict.keys()
        timeus = self.timeunit_dict.keys()
        ms = self.month_dict.keys()

    def match_timex(self, list_patterns):

        return re.findall('|'.join(list_patterns), self.tweet_text)

    def extract_date(self):

        list_patterns_date = (
            r'(\b|^)(\d{2}-\d{2}-\d{2,4})(\b|$)',
            r'(\b|^)(\d{4}-\d{2}-\d{2})(\b|$)',
            r'(\b|^)(\d{2}/\d{2})(/\d{2,4})?(\b|$)',
            r'(\b|^)(\d{4}/\d{2}/\d{2})(\b|$)'
        )

        matches = self.match_timex(list_patterns_date)
        if len(matches) > 0:
            for match in matches:
                datestring = ''.join([x for x in match if x != ''])
                refdate = time_functions.return_date(datefields)
                self.dates.append((datestring, refdate))

    def extract_timeunit(self):

        list_patterns_timeunits = ([r'(over|nog) (minimaal |maximaal |tenminste |bijna |ongeveer |maar |slechts |'
            r'pakweg |ruim |krap |(maar )?een kleine |(maar )?iets (meer|minder) dan )?' + (self.nums) + ' ' + 
            (self.timeunits) + r'($| )', (self.nums) + ' ' + (self.timeunits) + r'( slapen)? tot',
            r'met( nog)? (minimaal |maximaal |tenminste |bijna |ongeveer |maar |slechts |pakweg |ruim |'
            r'krap |(maar )?een kleine |(maar )?iets (meer|minder) dan )?' + (self.nums) + ' ' + (self.timeunits) + 
            r'( nog)? te gaan'])

        matches = self.match_timex(list_patterns_timeunits)
        if len(matches) > 0:
            for match in matches:
                timeunit_string = ''.join([x for x in match if x != ''])
                print(self.tweet_text.encode('utf-8'), timeunit_string)

            # for match in matches:
            #     for t in nud["timeunit"]: 
            #         num_match = t[1]
            #         if "num" in nud:
            #             try:
            #                 days = t[0] * [x[0] for x in nud["num"] if x[1] == num_match][0]
            #                 if days > 0:
            #                     output.append(date + datetime.timedelta(days=days))
            #             except:
            #                 continue


            #    datestring = ''.join([x for x in match if x != ''])
            #    refdate = time_functions.return_date(datefields)
            #    self.dates.append((datestring, refdate))

    #def extract_day():




        #     for da in nud["date"]:
        #         num_match = da[1]
        #         if re.search("-",da[0]):
        #             if "year" in nud:
        #                 if num_match in [x[1] for x in nud["year"]]:
        #                     ds = date_eu.search(da[0] + [x[0] for x in nud["year"] if x[1] == \
        #                         num_match][0]).groups()
        #                 else:
        #                     ds = date_eu.search(da[0]).groups()
        #             else:
        #                 ds = date_eu.search(da[0]).groups()
        #             dsi = [int(x) for x in ds if x != None]
        #             dsis = [x for x in ds if x != None]
        #             try:
        #                 if dsi[1] in range(1,13) and \
        #                     dsi[0] in range(1,32):
        #                     if ds[2] == None:
        #                         if not (len(dsis[0]) == 1 and len(dsis[1]) == 1): #avoid patterns like 1-2
        #                             y = decide_year(date,dsi[1],dsi[0])
        #                             if date < datetime.date(y,dsi[1],dsi[0]):
        #                                 output.append(datetime.date(y,dsi[1],dsi[0]))
        #                     else:
        #                         if dsi[2] in range(2010,2020):
        #                             if date < datetime.date(dsi[2],dsi[1],dsi[0]):
        #                                 output.append(datetime.date(dsi[2],dsi[1],dsi[0]))
        #                 elif dsi[0] in range(2010,2020): #2015/03/30
        #                     if dsi[1] in range(1,13) and dsi[2] in range(1,32):
        #                         if not (len(dsis[1]) == 1 and len(dsis[2]) == 1): #avoid patterns like 1/2
        #                             if date < datetime.date(dsi[0],dsi[1],dsi[2]):
        #                                 output.append(datetime.date(dsi[0],dsi[1],dsi[2]))
        #             except:
        #                 continue
        #         elif re.search("/",da[0]):
        #             if "year" in nud:
        #                 if num_match in [x[1] for x in nud["year"]]:
        #                     if [x[0] for x in nud["year"] if x[1] == num_match][0][-1] == "/":
        #                         ds = date_vs.search([x[0] for x in nud["year"] if x[1] == \
        #                             num_match][0] + da[0]).groups()
        #                     else:
        #                         ds = date_vs.search(da[0] + [x[0] for x in nud["year"] if x[1] == \
        #                             num_match][0]).groups()
        #                 else:
        #                     ds = date_vs3.search(da[0]).groups()
        #             else:
        #                 ds = date_vs3.search(da[0]).groups()
        #             dsi = [int(x) for x in ds if x != None]
        #             dsis = [x for x in ds if x != None]
        #             try:
        #                 if dsi[0] in range(1,13) and dsi[1] in range(1,32): #30/03/2015
        #                     outdate = False
        #                     if len(dsi) == 3:
        #                         if len(dsis[2]) == 4:
        #                             outdate = datetime.date(dsi[2],dsi[1],dsi[0])
        #                         elif len(dsis[2]) == 2:
        #                             if dsi[2] in range(10,21):
        #                                 outdate = datetime.date((dsi[2]+2000),dsi[1],dsi[0])
        #                     else:
        #                         if not (len(dsis[0]) == 1 and len(dsis[1]) == 1): #avoid patterns like 1/2
        #                             y = decide_year(date,dsi[1],dsi[0])
        #                             outdate = datetime.date(y,dsi[1],dsi[0])
        #                     if outdate:
        #                         if date < outdate:
        #                             output.append(outdate)
        #                 elif dsi[0] in range(1,13) and dsi[1] in range(1,32): #30/03
        #                     if not (len(dsis[0]) == 1 and len(dsis[1]) == 1): #avoid patterns like 1/2
        #                         y = decide_year(date,dsi[0],dsi[1])
        #                         if date < datetime.date(y,dsi[0],dsi[1]):
        #                             output.append(datetime.date(date.year,dsi[0],dsi[1]))
        #                 elif dsi[0] in range(2010,2020): #2015/03/30
        #                     if dsi[1] in range(1,13) and dsi[2] in range(1,32):
        #                         if not (len(dsis[1]) == 1 and len(dsis[2]) == 1): #avoid patterns like 1/2
        #                             if date < datetime.date(dsi[0],dsi[1],dsi[2]):
        #                                 output.append(datetime.date(dsi[0],dsi[1],dsi[2]))
        #             except:
        #                 continue



        # elif re.search(r"\d{1,2}-\d{1,2}",unit) or \
        #     re.search(r"\d{1,2}/\d{1,2}",unit): #date 
        #     nud["date"].append((unit,i))
        #     timephrases[i] = "".join([x for x in units if len(x) > 0 and not x == " "])
        # elif re.search(r"-\d{2,4}",unit) or re.search(r"\d{4}-",unit) or re.search(r"\d{4}/",unit) or re.search(r"/\d{2,4}",unit): #year
        #     nud["year"].append((unit,i))
>>>>>>> c01129e364dd08ba5c3c369193830b20143433c4



#             timephrases = []
#             matches = re.findall('|'.join(list_patterns), tweet_text)
#             nud = defaultdict(list)

#             # for all matches
#             for i,units in enumerate(matches):

#                 # select timephrases
#                 timephrases.append(" ".join([x for x in units if len(x) > 0 and not x == " "]))
                
#                 # for all timephrase parts
#                 for unit in units:

#                     # classify type
#                     if unit in ns: # number
#                         nud["num"].append((convert_nums[unit],i))
#                     elif unit in timeus: # time unit
#                         if not "weekday" in nud:
#                             nud["timeunit"].append((convert_timeunit[unit],i))
#                     elif unit in ms: # month
#                         nud["month"].append((convert_month[unit],i))
#                     elif re.search(r"\d{1,2}-\d{1,2}",unit) or \
#                         re.search(r"\d{1,2}/\d{1,2}",unit): #date 
#                         nud["date"].append((unit,i))
#                         timephrases[i] = "".join([x for x in units if len(x) > 0 and not x == " "])
#                     elif re.search(r"-\d{2,4}",unit) or re.search(r"\d{4}-",unit) or re.search(r"\d{4}/",unit) or re.search(r"/\d{2,4}",unit): #year
#                         nud["year"].append((unit,i))
#                     elif re.match(r"\d+",unit): #digit
#                         if int(unit) in range(2010,2020):
#                             nud["year"].append((int(unit),i)) #year
#                         elif "num" in nud: 
#                             if int(unit) in range(1,13): # month
#                                 nud["month"].append((int(unit),i))
#                             nud["num"].append((int(unit),i)) # number
#                         else:
#                             nud["num"].append((int(unit),i)) # number
#                     elif unit in weekdays:
#                         nud["weekday"].append((unit,i)) #weekday
#                         if re.search(unit + r"(avond|middag|ochtend|nacht)",tweet_text):
#                             timephrases[i] = "".join([x for x in units if len(x) > 0 and not x == " "])
#                     elif unit in spec_days:
#                         nud["sday"].append((unit,i)) # overmorgen / morgen
#                     elif unit == "volgende week":
#                         nud["nweek"].append((unit,i)) # week
#                 timephrases[i] = timephrases[i].replace("  "," ")
#             regexPattern = '|'.join(map(re.escape, timephrases))
#             tp = ', '.join(timephrases)
#             output = [re.split(regexPattern, tweet_text),tp]


#         if "month" in nud:
#             for t in nud["month"]:
#                 num_match = t[1]
#                 m = t[0]
#                 try:
#                     d = [x[0] for x in nud["num"] if x[1] == num_match][0]
#                     if "year" in nud:
#                         if num_match in [x[1] for x in nud["year"]]:
#                             y = [x[0] for x in nud["year"] if x[1] == num_match][0]
#                         else:
#                             y = decide_year(date,m,d)
#                     else:
#                         y = decide_year(date,m,d)
#                     if date < datetime.date(y,m,d):
#                         output.append(datetime.date(y,m,d))
#                 except:
#                     continue

#         if "weekday" in nud:
#             if not "date" in nud and not "month" in nud and not "timeunit" in nud: # overrule by more specific indication
#                 tweet_weekday=date.weekday()
#                 for w in nud["weekday"]:
#                     num_match = w[1]
#                     ref_weekday=weekdays.index(w[0])
#                     if num_match in [x[1] for x in nud["nweek"]]:
#                         add = 7
#                     else:
#                         add = 0
#                     if not ref_weekday == tweet_weekday and not num_match in [x[1] for x in nud["nweek"]]: 
#                         if tweet_weekday < ref_weekday:
#                             days_ahead = ref_weekday - tweet_weekday + add
#                         else:
#                             days_ahead = ref_weekday + (7-tweet_weekday) + add
#                         output.append(date + datetime.timedelta(days=days_ahead))
#         if "sday" in nud:
#             for s in nud["sday"]:
#                 num_match = s[1] 
#                 timephrase = " ".join([x for x in matches[num_match] if len(x) > 0])
#                 u = s[0]
#                 if u == "overmorgen":
#                     output.append(date + datetime.timedelta(days=2))
#                 elif u == 'morgen':
#                     output.append(date + datetime.timedelta(days=1))
#         if len(nud.keys()) == 0:
#             return False
#         else:
#             return output


