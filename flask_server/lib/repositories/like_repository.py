from lib.models.like import Like

class LikeRepository:
    def __init__(self, connection):
        self._connection = connection

    # I will refer to Like instances as like_events. (ie action of a user liking a post or comment.)

    # == ALL LIKE EVENTS ================

    def all(self) -> list[Like]:
        rows = self._connection.execute('SELECT * FROM likes')
        like_events = []
        for row in rows:
            like_event = Like(row['id'], row['user_id'], row['post_id'], row['comment_id'])
            like_events.append(like_event)
        return like_events
    
    # # == FIND LIKE EVENTS ================

    def find_event_by_id(self, like_event_id) -> Like:
        rows = self._connection.execute('SELECT * FROM likes WHERE id = %s',[like_event_id])
        row = rows[0]
        return Like(row['id'], row['user_id'], row['post_id'], row['comment_id'])
    
    def find_event_id_by_details(self, user_id, post_id=None, comment_id=None) -> int or None:
        # if post_id is None, the content is a comment. If comment_id is None, the content is a post.
        # users can only like a piece of content once, so result is None or a single event id
        if comment_id == None:       
            rows = self._connection.execute('SELECT * FROM likes WHERE user_id=%s AND post_id=%s', [user_id, post_id])
        elif post_id == None:
            rows = self._connection.execute('SELECT * FROM likes WHERE user_id=%s AND comment_id=%s', [user_id, comment_id])
        if rows == []:
            return None #no event found
        return rows[0]['id']

    # # == LIKE A POST OR COMMENT ===============
    def check_if_already_liked(self, user_id, post_id=None, comment_id=None) -> bool: 
        # TODO -- a bit redundant. do this in app.py?
        # TODO -- decide on useage -- to generate errors or to change button function?:
        # Option 1: If already liked, turn button to Unlike. If not liked,  then Like button
        if self.find_event_id_by_details(user_id, post_id, comment_id) == None:
            return False #not liked yet -- can only #like
        return True #already liked -- can only #unlike

    def like(self, user_id, post_id=None, comment_id=None) -> int:
        # Same as create() for a basic crud app, but we are calling the method by the colloquial term for easy comprehension
        # validity checked externally
        rows = self._connection.execute('INSERT INTO likes (user_id, post_id, comment_id) VALUES (%s, %s, %s) RETURNING id', [user_id, post_id, comment_id])
        like_event_id = rows[0]['id']
        return like_event_id

    # == UNLIKE A POST/COMMENT ===============
    def unlike(self, user_id, post_id=None, comment_id=None) -> None:
        # Same as delete() for a basic crud app, but we are calling the method by the colloquial term for easy comprehension
        event_id = self.find_event_id_by_details(user_id=user_id, post_id=post_id, comment_id=comment_id)
        self._connection.execute('DELETE FROM likes WHERE id=%s', [event_id])
        return None

    # ======== INTEGRATION =======================================

    ## == FIND ALL USERS WHO LIKED THIS -- moved to Users =========================
    def who_liked_this(self, post_id=None, comment_id=None) -> list[int]:
        # Coverage for post and comment without extra writing
        if post_id == None: 
            rows = self._connection.execute('SELECT users.id, users.email, users.password, users.handle, users.name, users.joined_on FROM users JOIN likes ON users.id = likes.user_id WHERE likes.comment_id=%s', [comment_id])
        elif comment_id == None:
            rows = self._connection.execute('SELECT users.id, users.email, users.password, users.handle, users.name, users.joined_on FROM users JOIN likes ON users.id = likes.user_id WHERE likes.post_id=%s', [post_id])
        return rows

    def total_likes(self, post_id=None, comment_id=None) -> int:
        return len(self.who_liked_this(post_id, comment_id))

    ## == FIND ALL OF ONE USER's POST LIKES ==========================
    def find_all_posts_liked_by_user(self, user_id) -> list[int]:
        rows = self._connection.execute('SELECT posts.id FROM posts JOIN likes ON posts.id = likes.post_id WHERE likes.user_id = %s', [user_id])
        posts = []
        for row in rows:
            post = row['id']
            # Post object instead?
            posts.append(post)
        return posts

    ## == FIND ALL OF ONE USER's COMMENT LIKES ==========================
    def find_all_comments_liked_by_user(self, user_id) -> list[int]:
        rows = self._connection.execute('SELECT comments.id FROM comments JOIN likes ON comments.id = likes.comment_id WHERE likes.user_id = %s', [user_id])
        comments = []
        for row in rows:
            comment = row['id']
            # Comment object instead?
            comments.append(comment)
        return comments
    
    ## == FIND ALL LIKES ON ONE POST =========================
    