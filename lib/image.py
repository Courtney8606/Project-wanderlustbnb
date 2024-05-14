class Image:
    #Set object attributes
    def __init__(self, id, title):
        self.id = id
        self.title = title

    # Equality method
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # Formatting
    def __repr__(self):
        return f"Image({self.id}, {self.title})"
