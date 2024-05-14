class User:
    # Initialise with all of our attributes
    def __init__(self, id, username, name, password):
        self.id = id
        self.username = username
        self.name = name
        self.password = password

    # Equality method
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    # Formatting
    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.name}, {self.password})"
