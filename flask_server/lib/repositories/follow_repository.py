from lib.models.follow import Follow
from lib.models.user import User

class FollowRepository:
    def __init__(self, connection):
        self._connection = connection

    # I will refer to Follow instances as follow_events. (ie action of a user following another user.)
    # For find all followers and find all following for a particular user, we will use the colloquial syntax (ie. find_followers(user_id) is users who follow user_id)

    # == ALL FOLLOW EVENTS ================

    def all(self) -> list[Follow]:
        rows = self._connection.execute('SELECT * FROM follows')
        follow_events = []
        for row in rows:
            follow_event = Follow(row['id'], row['follower_id'], row['followee_id'])
            follow_events.append(follow_event)
        return follow_events
    
    # # == FIND FOLLOW EVENTS ================

    def find_event_by_id(self, follow_event_id) -> Follow:
        rows = self._connection.execute('SELECT * FROM follows WHERE id = %s',[follow_event_id])
        row = rows[0]
        return Follow(row['id'], row['follower_id'], row['followee_id'])
    
    def find_event_by_users(self, follower_id, followee_id) -> int or None:
        rows = self._connection.execute('SELECT * FROM follows WHERE follower_id=%s AND followee_id=%s', [follower_id, followee_id])
        # users can only like another user once, so either 1 or 0 rows will be found
        if rows == []:
            return None #no event found
        return rows[0]['id']

    # # == FOLLOW ANOTHER USER ===============
    def check_if_already_following(self, follower_id, followee_id) -> bool: 
        # TODO -- a bit redundant. do this in app.py?
        # TODO -- decide on useage -- to generate errors or to change button function?:
        # Option 1: If already following, turn button to Unfollow. If not following,  then Follow button
        if self.find_event_by_users(follower_id, followee_id) == None:
            return False #not following yet -- can only #follow
        return True #already following -- can only #unfollow

    def check_if_valid(self, follower_id, followee_id) -> bool:
        # users cannot follow their own profile
        if follower_id == followee_id:
            return False
        return True

    def follow(self, follower_id, followee_id) -> int:
        # Same as create() for a basic crud app, but we are calling the method by the colloquial term for easy comprehension
        # validity checked externally
        rows = self._connection.execute('INSERT INTO follows (follower_id, followee_id) VALUES (%s, %s) RETURNING id', [follower_id, followee_id])
        follow_event_id = rows[0]['id']
        return follow_event_id

    # == UNFOLLOW ANOTHER USER ===============
    def unfollow(self, follower_id, followee_id) -> None:
        # Same as delete() for a basic crud app, but we are calling the method by the colloquial term for easy comprehension
        self._connection.execute('DELETE FROM follows WHERE follower_id=%s AND followee_id=%s', [follower_id, followee_id]) #we can do this instead of follow_event_id because users can only follow another user once.
        return None