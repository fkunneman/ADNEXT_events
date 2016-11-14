
import re

class CityrefExtractor:

    def __init__(self,citylist):
        # make sure that the longest citynames are on top and are privileged in pattern matching
        self.cities_lowercase = self.cities2lowercase(citylist)
        citylist_lowercase = list(self.cities_lowercase.keys())
        self.citylist = self.sort_citylist(citylist_lowercase) 
        self.startpatterns = self.return_patterns_startofstring(self.citylist)
        self.patterns = self.return_patterns_middle(self.citylist)
        self.endpatterns = self.return_patterns_endofstring(self.citylist)
        self.cityrefs_start = []        
        self.cityrefs_middle = []
        self.cityrefs_end = []

    def return_patterns_startofstring(self,citylist):
        return '|'.join(['^' + x + '[^\w]' for x in citylist])
        
    def return_patterns_middle(self,citylist):
        return '|'.join(['[^\w]' + x + '[^\w]' for x in citylist])

    def return_patterns_endofstring(self,citylist):
        return '|'.join(['[^\w]' + x + '$' for x in citylist])

    def return_patterns(self,citylist):
        return '|'.join([self.return_patterns_startofstring(citylist),self.return_patterns_middle(citylist),self.return_patterns_endofstring(citylist)])

    def sort_citylist(self,citylist):
        return sorted(citylist,key = lambda k : len(k),reverse=True)

    def cities2lowercase(self,citylist):
        cities_lowercase = dict([(cityname.lower(),cityname) for cityname in citylist])
        return cities_lowercase

    def find_cityrefs(self,string):
        self.cityrefs_start.extend(re.findall(self.startpatterns,string))
        self.cityrefs_middle.extend(re.findall(self.patterns,string))
        self.cityrefs_end.extend(re.findall(self.endpatterns,string))

    def return_capitalized(self,cityrefs,startofstring,endofstring):
        if endofstring:
            return [self.cities_lowercase[cityref[startofstring:endofstring]] for cityref in cityrefs]
        else:
            return [self.cities_lowercase[cityref[startofstring:]] for cityref in cityrefs]

    def return_cityrefs(self):
        cityrefs = list(set(sum([self.return_capitalized(self.cityrefs_start,0,-1),self.return_capitalized(self.cityrefs_middle,1,-1),self.return_capitalized(self.cityrefs_end,1,False)], [])))

        return cityrefs 
