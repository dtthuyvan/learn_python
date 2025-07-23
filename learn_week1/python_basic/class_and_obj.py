class Member:
    def __init__(self, name, age, joined_date, address = 'None'):
        self.name = name
        self.age = age
        self.joined_date = joined_date
        self.address = address
    
    def __str__(self):
        return f"{self.name}, age {self.age}, joined at {self.joined_date}, address {self.address}"