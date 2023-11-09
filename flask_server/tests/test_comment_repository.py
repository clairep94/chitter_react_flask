from lib.repositories.comment_repository import Comment, CommentRepository
from datetime import datetime

## COMMENT CLASS ###

def test_comment_eq():
    comment1 = Comment(comment_id=1, post_id=1, user_id=1, content= "this is a test", created_on=datetime(2023,10,20,12,30,0))
    comment2 = Comment(comment_id=1, post_id=1, user_id=1, content= "this is a test", created_on=datetime(2023,10,20,12,30,0))

    assert comment1 == comment2

def test_hashtag_repr():
    comment1 = Comment(1, 1, 1, "this is a test", datetime(2023,10,20, 12, 30, 0))
    print(comment1.created_on)
    print(type(comment1.created_on))
    assert str(comment1) == "Comment(1, User #1 commented on Post #1)"

##############################################

## COMMENT REPO UNIT ##################

# === ALL COMMENTS =========== #
def test_all_comments(db_connection):
    '''
    When we call all, we get all like comments in our db
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = CommentRepository(db_connection)
    assert repository.all() == [
        Comment(1, 1, 2, "Yes it was sooo good!", datetime(2023,10,16,19,5,0)),
        Comment(2, 1, 3, 'the scene where david asked posh about her dads car lollll', datetime(2023, 10, 16, 23, 15, 0)),
        Comment(3, 2, 3, "classic", datetime(2023, 10, 17, 13, 47, 0))
    ]

# === FIND BY =========== #
def test_find_by_id(db_connection):
    '''
    We can find a comment by its comment_id
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = CommentRepository(db_connection)
    assert repository.find_by_id(1) == Comment(1, 1, 2, "Yes it was sooo good!", datetime(2023,10,16,19,5,0))

def test_find_all_for_post(db_connection):
    '''
    We can find all comments for an individual post
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = CommentRepository(db_connection)
    assert repository.find_all_for_post(1) == [
        Comment(1, 1, 2, "Yes it was sooo good!", datetime(2023,10,16,19,5,0)),
        Comment(2, 1, 3, 'the scene where david asked posh about her dads car lollll', datetime(2023, 10, 16, 23, 15, 0))
    ]


# === CREATE =========== #
def test_check_content_valid_errors(db_connection):
    '''
    When we create content, we have to be logged in and the content entry has to be not empty, otherwise we generate errors.
    If we have any hashtags, we separate them into a list
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = CommentRepository(db_connection)

    assert repository.check_content_valid_errors(None, None) == "Please log in to create a comment."
    assert repository.check_content_valid_errors(None, "some content") == "Please log in to create a comment."
    assert repository.check_content_valid_errors(1, None) == "Comment content cannot be empty."
    assert repository.check_content_valid_errors(1, "finally valid") == None

def test_create(db_connection):
    '''
    When we create a comment, we can see it in the all comments
    We can see it in the user's comments
    We can see it in the post's comments
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = CommentRepository(db_connection)

    assert repository.create(post_id=1, user_id=2, content="I know lmaoo", created_on=datetime(2023, 10, 21, 12, 52, 0)) == 4
    assert repository.all() == [
        Comment(1, 1, 2, "Yes it was sooo good!", datetime(2023,10,16,19,5,0)),
        Comment(2, 1, 3, 'the scene where david asked posh about her dads car lollll', datetime(2023, 10, 16, 23, 15, 0)),
        Comment(3, 2, 3, "classic", datetime(2023, 10, 17, 13, 47, 0)),
        Comment(4, 1, 2, "I know lmaoo", datetime(2023, 10, 21, 12, 52, 0))
    ]
    assert repository.find_all_for_post(1) == [
        Comment(1, 1, 2, "Yes it was sooo good!", datetime(2023,10,16,19,5,0)),
        Comment(2, 1, 3, 'the scene where david asked posh about her dads car lollll', datetime(2023, 10, 16, 23, 15, 0)),
        Comment(4, 1, 2, "I know lmaoo", datetime(2023, 10, 21, 12, 52, 0))
    ]
    assert repository.find_all_by_user(2) == [
        Comment(1, 1, 2, "Yes it was sooo good!", datetime(2023,10,16,19,5,0)),
        Comment(4, 1, 2, "I know lmaoo", datetime(2023, 10, 21, 12, 52, 0))
    ]

# === DELETE ========== #
def test_delete(db_connection):
    '''
    When we delete a comment
    We will no longer see it in all comments
    We will no longer see it in the user's comments
    We will no longer see it in the post's comments
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = CommentRepository(db_connection)

    repository.delete(1)
    assert repository.all() == [
        Comment(2, 1, 3, 'the scene where david asked posh about her dads car lollll', datetime(2023, 10, 16, 23, 15, 0)),
        Comment(3, 2, 3, "classic", datetime(2023, 10, 17, 13, 47, 0))
    ]
    assert repository.find_all_by_user(2) == []
    assert repository.find_all_for_post(1) == [
        Comment(2, 1, 3, 'the scene where david asked posh about her dads car lollll', datetime(2023, 10, 16, 23, 15, 0))
    ]



# === SORT BY ========== #
def test_sort_by_descending_date(db_connection):
    '''
    When we feed in a list of comments, we can retrieve them in order of most recent to oldest
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = CommentRepository(db_connection)

    assert repository.sort_by_descending_date(repository.all()) == [
        Comment(3, 2, 3, "classic", datetime(2023, 10, 17, 13, 47, 0)),
        Comment(2, 1, 3, 'the scene where david asked posh about her dads car lollll', datetime(2023, 10, 16, 23, 15, 0)),
        Comment(1, 1, 2, "Yes it was sooo good!", datetime(2023,10,16,19,5,0))
    ]



## ============================================================================ ##
## ======== INTEGRATION ======================================================= ##
## ============================================================================ ##

# ========= USER ======================
def test_all_by_user(db_connection):
    '''
    We can find all comments by a user
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = CommentRepository(db_connection)

    assert repository.find_all_by_user(1) == []
    assert repository.find_all_by_user(3) == [
        Comment(2, 1, 3, 'the scene where david asked posh about her dads car lollll', datetime(2023, 10, 16, 23, 15, 0)),
        Comment(3, 2, 3, "classic", datetime(2023, 10, 17, 13, 47, 0))
    ]




# ========= LIKES ======================

def test_sort_by_likes(db_connection):
    '''
    When we feed in a list of comments, we can retrieve them in order of most likes to least
    if most_popular=False, we sort by least likes to most likes.
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = CommentRepository(db_connection)

    # assert repository.sort_by_likes(repository.all()) == 
    assert repository.sort_by_likes(repository.all()) == [
        {"comment": Comment(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)), "likes_count": 2},
        {"comment": Comment(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)), "likes_count": 1},
        {"comment": Comment(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0)), "likes_count": 1}
    ]
    assert repository.sort_by_likes(repository.all(), most_popular=False) == [
        {"comment": Comment(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0)), "likes_count": 1},
        {"comment": Comment(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)), "likes_count": 1},
        {"comment": Comment(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)), "likes_count": 2}
    ]
    repository.unlike(1) #user 3 liked comment 1
    assert repository.sort_by_likes(repository.all()) == [
        {"comment": Comment(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)), "likes_count": 2},
        {"comment": Comment(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0)), "likes_count": 1},
        {"comment": Comment(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)), "likes_count": 0}        
    ]
