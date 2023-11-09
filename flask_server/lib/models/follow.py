class Follow:
    def __init__(self, follow_id, follower_id, followee_id) -> None:
        self.follow_event_id = follow_id
        self.follower_id = follower_id
        self.followee_id = followee_id

    def __eq__(self, other):
        if not isinstance(other, Follow):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Follow({self.follow_event_id}, User #{self.follower_id} followed User #{self.followee_id})"