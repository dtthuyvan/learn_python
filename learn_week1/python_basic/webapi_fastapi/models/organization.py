
# Define request body
class Organization:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __str__(self):
        return f"{self.name}, id {self.id}"