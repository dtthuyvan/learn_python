class TourGuide:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        print(F"name {self.name} (id:{self.id})")