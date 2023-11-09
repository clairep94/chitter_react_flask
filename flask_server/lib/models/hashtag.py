class Hashtag:
    def __init__(self, hashtag_id:int, title:str):
        self.hashtag_id = hashtag_id
        self.title = title

    # This method allows our tests to assert that the objects it expects
    # are the objects we made based on the database records.
    def __eq__(self, other):
        if not isinstance(other, Hashtag):
            return False

        return self.__dict__ == other.__dict__

    # This method makes it look nicer when we print an Users
    def __repr__(self):
        return f"Hashtag({self.hashtag_id}, {self.title})"
