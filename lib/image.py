class Image:
    # We initialise with all of our attributes
    # Each column in the table should have an attribute here
    def __init__(self, id, title):
        self.id = id
        self.title = title

    # This method allows our tests to assert that the objects it expects
    # are the objects we made based on the database records.
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
