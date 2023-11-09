class Like:
    def __init__(self, like_event_id, user_id, post_id, comment_id) -> None:
        self.like_event_id = like_event_id
        self.user_id = user_id
        self.post_id = post_id #none if like is on a comment
        self.comment_id = comment_id #none if like is on a post.
    
    def __eq__(self, other):
        if not isinstance(other, Like):
            return False
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        if self.post_id == None:
            return f"Like({self.like_event_id}, User #{self.user_id} liked Comment #{self.comment_id})"
        return f"Like({self.like_event_id}, User #{self.user_id} liked Post #{self.post_id})"