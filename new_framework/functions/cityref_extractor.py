
import re

class CityrefExtractor:

    def __init__(self,citylist):
        # make sure that the longest citynames are on top and are privileged in pattern matching
        self.cities_lowercase = self.cities2lowercase(citylist)
        citylist_lowercase = list(self.cities_lowercase.keys())
        sorted_citylist = self.sort_citylist(citylist_lowercase) 
        self.citypatterns = '|'.join(sorted_citylist)
        self.cityrefs = []        

    def sort_citylist(self,citylist):
        return sorted(citylist,key = lambda k : len(k),reverse=True)

    def cities2lowercase(self,citylist):
        cities_lowercase = dict([(cityname.lower(),cityname) for cityname in citylist])
        return cities_lowercase

    def find_cityrefs(self,string):
        matches = re.findall(self.citypatterns,string)
        self.cityrefs.extend(matches)

    def return_cityrefs(self):
        return [self.cities_lowercase[cityref] for cityref in list(set(self.cityrefs))] 
