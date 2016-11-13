
class CityrefExtractor:

    def __init__(self,citylist):
        self.citylist = citylist
        self.cityrefs = []        

    def return_cities(self,string):
        matches = re.findall(self.citylist,string)
        print(matches)
