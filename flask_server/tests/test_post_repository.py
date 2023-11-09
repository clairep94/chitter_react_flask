from lib.repositories.post_repository import Post, PostRepository
from datetime import datetime

## POST CLASS ###

def test_post_eq():
    post1 = Post(1, 1, "this is a test", datetime(2023,10,20,12,30,0))
    post2 = Post(1, 1, "this is a test", datetime(2023,10,20,12,30,0))
    assert post1 == post2

def test_hashtag_repr():
    post1 = Post(1, 1, "this is a test", datetime(2023,10,20, 12, 30, 0))
    print(post1.created_on)
    print(type(post1.created_on))
    assert str(post1) == "Post(1, User #1 created Post #1 on 2023-10-20 12:30:00)"

##############################################

## POST REPO UNIT ##################

# === ALL POSTS =========== #
def test_all_posts(db_connection):
    '''
    When we call all, we get all like posts in our db
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)
    assert repository.all() == [
        Post(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)),
        Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)),
        Post(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0))
    ]

# === FIND BY =========== #
def test_find_by_id(db_connection):
    '''
    We can find a post by its post_id
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)
    assert repository.find_by_id(1) == Post(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0))

def test_find_by_hashtag(db_connection):
    '''
    We can find all posts with a certain hashtag
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)

    repository.find_by_hashtag("football") == [        
        Post(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)),
        Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0))
    ]
    repository.find_by_hashtag("soccer") == []


# === CREATE =========== #
def test_check_content_valid_errors(db_connection):
    '''
    When we create content, we have to be logged in and the content entry has to be not empty, otherwise we generate errors.
    If we have any hashtags, we separate them into a list
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)

    assert repository.check_content_valid_errors(None, None) == "Please log in to create a post."
    assert repository.check_content_valid_errors(None, "some content") == "Please log in to create a post."
    assert repository.check_content_valid_errors(1, None) == "Post content cannot be empty."
    assert repository.check_content_valid_errors(1, "finally valid") == None

def test_create(db_connection):
    '''
    When we create a post, we can see it in the all posts
    We can see it in the user's posts
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)

    assert repository.create(1, "new content", datetime(2023, 10, 21, 12, 52, 0)) == 4
    assert repository.all() == [
        Post(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)),
        Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)),
        Post(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0)),
        Post(4, 1, "new content", datetime(2023, 10, 21, 12, 52, 0))
    ]

# === DELETE ========== #
def test_delete(db_connection):
    '''
    When we delete a post
    We will no longer see it in all posts
    We will no longer see it in the user's posts
    ** We will no longer see its comments in all comments 
    ** We will no longer see the comments in their respective poster's comments    
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)

    repository.delete(1)
    assert repository.all() == [
        Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)),
        Post(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0))
    ]
    assert repository.find_all_by_user(1) == [
        Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0))
    ]



# === SORT BY ========== #
def test_sort_by_descending_date(db_connection):
    '''
    When we feed in a list of posts, we can retrieve them in order of most recent to oldest
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)

    assert repository.sort_by_descending_date(repository.all()) == [
        Post(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0)),
        Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)),
        Post(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0))
    ]



## ============================================================================ ##
## ======== INTEGRATION ======================================================= ##
## ============================================================================ ##

# ========= USER ======================
def test_all_posts_by_user(db_connection):
    '''
    We can find all posts by a user
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)

    assert repository.find_all_by_user(1) == [
        Post(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)),
        Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0))
    ]


# ========= HASHTAGS ===================
def test_generate_hashtags(db_connection):
    '''
    We can search through the content of a post when it is created and generate hashtags -- strings starting with #, separated by whitespace
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)

    assert repository.generate_hashtags("test content no hashtags") == []
    assert repository.generate_hashtags("# # # #actual hastag") == ["actual"] 
    assert repository.generate_hashtags("Another example of a #hashtag and a non#hashtag and another #tag") == ["hashtag", "tag"]




# ========= LIKES ======================

def test_sort_by_likes(db_connection):
    '''
    When we feed in a list of posts, we can retrieve them in order of most likes to least
    if most_popular=False, we sort by least likes to most likes.
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = PostRepository(db_connection)

    # assert repository.sort_by_likes(repository.all()) == 
    assert repository.sort_by_likes(repository.all()) == [
        {"post": Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)), "likes_count": 2},
        {"post": Post(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)), "likes_count": 1},
        {"post": Post(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0)), "likes_count": 1}
    ]
    assert repository.sort_by_likes(repository.all(), most_popular=False) == [
        {"post": Post(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0)), "likes_count": 1},
        {"post": Post(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)), "likes_count": 1},
        {"post": Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)), "likes_count": 2}
    ]
    repository.unlike(1) #user 3 liked post 1
    assert repository.sort_by_likes(repository.all()) == [
        {"post": Post(2, 1, '"football" not "soccer", tyvm', datetime(2023, 10, 17, 10, 30, 0)), "likes_count": 2},
        {"post": Post(3, 2, "I am once again asking for your financial support", datetime(2023, 10, 17, 11, 9, 0)), "likes_count": 1},
        {"post": Post(1, 1, "Has anyone seen the new David Beckham series?", datetime(2023,10,16,12,30,0)), "likes_count": 0}        
    ]
