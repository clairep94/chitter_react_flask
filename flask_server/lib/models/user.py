from datetime import datetime
class User:
    # We initialise with all of our attributes
    # Each column in the table should have an attribute here
    def __init__(self, user_id:int, email:str, password:str, handle:str, name:str, joined_on:datetime=None):
        self.user_id = user_id 
        self.email = email
        # TODO: Something with hashing password here, or in user_repository#Create
        self.password = password 
        self.handle = handle # @AOC
        self.name = name # Alexandria Ocasio-Cortez
        self.joined_on = joined_on # Joined April 2017; datetime.date on user_repository#Create
        
    # This method allows our tests to assert that the objects it expects
    # are the objects we made based on the database records.
    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.__dict__ == other.__dict__

    # This method makes it look nicer when we print an Users
    def __repr__(self):
        return f"User({self.user_id}, Display Name: {self.name}, Handle: @{self.handle})"
