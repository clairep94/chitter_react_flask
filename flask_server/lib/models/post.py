class Post:
    def __init__(self, post_id:int, user_id:int, content:str, created_on) -> None:
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.created_on = created_on #datetime.date objet

    
    def __eq__(self, other):
        if not isinstance(other, Post):
            return False

        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f"Post({self.post_id}, User #{self.user_id} created Post #{self.post_id} on {self.created_on})"    

    # ========= DISPLAY ========================
    # calculate date for display -- move to Post method
    # find user_data for display -- move to Post method
    # display all likes -- move to Post method
