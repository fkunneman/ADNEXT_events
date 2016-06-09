

class Tweet:
    """
    Class containing the characteristics of a tweet that mentions 
        an entity and time
    """
    def __init__(self, ):


    def set_meta(self,units):
        self.id = units[0]
        self.user = units[1]
        self.date = units[2]
        self.text = units[3]
        self.daterefs = units[4]
        self.chunks = units[5]

    def set_entities(self,entities):
        if len(entities) == 0:
            self.entities = ["--"]
        else:
            self.entities = entities
            self.e = True

    def set_postags(self,tags):
        if len(tags) == 0:
            self.postags = [("--","--")]
        else:
            self.postags = tags

    def set_phrase(self,phrase):
        self.phrase = phrase

    def set_cities(self,cities):
        if len(cities) == 0:
            self.cities = ["--"]
        else:
            self.cities = cities