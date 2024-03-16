class Space():
    def __init__(self, id, name, location, price, description, user_id, image_title):
        self.id = id
        self.name = name
        self.location = location
        self.price = price
        self.description = description
        self.user_id = user_id
        self.image_title = image_title

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Space({self.id}, {self.name}, {self.location}, {self.price}, {self.description}, {self.user_id}, {self.image_title})"
