from lib.models.like import Like
from lib.repositories.like_repository import LikeRepository

## FOLLOW CLASS ###

def test_like_eq():
    event1 = Like(1, 1, 2, None)
    event2 = Like(1, 1, 2, None)
    assert event1 == event2

def test_like_repr():
    event1 = Like(1, 1, 2, None) #post
    event2 = Like(like_event_id=1, user_id=1, post_id=None, comment_id=2) #comment
    assert str(event1) == "Like(1, User #1 liked Post #2)"
    assert str(event2) == "Like(1, User #1 liked Comment #2)"


##############################################

## FOLLOW REPO UNIT ##########

def test_get_all_like_events(db_connection):
    '''
    When we call all, we get all like events in our db
    '''
    # Probably won't use this on our website
    db_connection.seed("seeds/chwitter.sql")
    repository = LikeRepository(db_connection)

    like_events = repository.all()
    assert like_events == [
        Like(1, 3, 1, None),
        Like(2, 2, 2, None),
        Like(3, 3, 2, None),
        Like(4, 3, 3, None),
        Like(5, 2, None, 3)
    ]

def test_find_event_by_id(db_connection):
    '''
    We can find a like event by the like_event_id
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = LikeRepository(db_connection)

    like_event = repository.find_event_by_id(1)
    assert like_event == Like(1, 3, 1, None)

def test_find_event_id_by_details(db_connection):
    '''
    We can find the id of the like event by providing the user id and the post or comment id.
    If the event does not exist, we get None.
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = LikeRepository(db_connection)

    like_event = repository.find_event_id_by_details(3, 1, None)
    assert like_event == 1
    like_event = repository.find_event_id_by_details(3, None, 1)
    assert like_event == None


def test_check_if_already_liked(db_connection):
    '''
    If the user is already liking the desired post or comment, we get True (already liking.) Otherwise we get False (not yet liking).
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = LikeRepository(db_connection)

    # user has not liked post or comment
    like_event = repository.find_event_id_by_details(1, None, 3)
    assert like_event == None
    assert repository.check_if_already_liked(1, None, 3) == False

    # user has already liked post or comment
    like_event = repository.find_event_id_by_details(3, 1, None)
    assert like_event == 1
    assert repository.check_if_already_liked(3, 1, None) == True


def test_like(db_connection):
    '''
    When a user likes a post or comment, we create a like event.
    When we call #all, we can see the new like event in the list of events.
    '''
    # TODO We can see the new user_ids in the list of who likes this post.
    # TODO when we delete a user, we no longer see the user among the posts' likers
    db_connection.seed("seeds/chwitter.sql")
    repository = LikeRepository(db_connection)

    assert repository.like(1, 3, None) == 6
    assert repository.all() == [
        Like(1, 3, 1, None),
        Like(2, 2, 2, None),
        Like(3, 3, 2, None),
        Like(4, 3, 3, None),
        Like(5, 2, None, 3),
        Like(6, 1, 3, None)
    ]
    # assert repository.who_liked_this(3, None) == [3, 1] ## Covered in users

def test_unlike(db_connection):
    '''
    When one user unlikes a post or comment, we delete the like event
    When we call #all, we can see the event has been deleted in the list of events.
    We can longer see the user_id in the list of who likes this.
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = LikeRepository(db_connection)

    repository.unlike(3, 1, None)
    assert repository.all() == [
        Like(2, 2, 2, None),
        Like(3, 3, 2, None),
        Like(4, 3, 3, None),
        Like(5, 2, None, 3)
    ]
    # assert repository.who_liked_this(1, None) == [] ## Covered in users

def total_likes(db_connection):
    '''
    We can see the number of people who like this post or comment
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = LikeRepository(db_connection)
    assert repository.total_likes(post_id=2) == 2
    assert repository.total_likes(comment_id=2) == 0

def test_find_all_posts_liked_by_user(db_connection):
    '''
    We can see a list of all posts liked by a user
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = LikeRepository(db_connection)
    assert repository.find_all_posts_liked_by_user(2) == [2]

def test_find_all_comments_liked_by_user(db_connection):
    '''
    We can see a list of all commentss liked by a user
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = LikeRepository(db_connection)
    assert repository.find_all_comments_liked_by_user(2) == [3]
