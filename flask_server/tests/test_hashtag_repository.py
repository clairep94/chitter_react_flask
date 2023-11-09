from lib.repositories.hashtag_repository import Hashtag, HashtagRepository

## HASHTAG CLASS ###

def test_hashtag_eq():
    hashtag1 = Hashtag(1, "memes")
    hashtag2 = Hashtag(1, "memes")
    assert hashtag1 == hashtag2

def test_hashtag_repr():
    hashtag1 = Hashtag(1, "memes")
    assert str(hashtag1) == "Hashtag(1, memes)"


##############################################

## HASHTAG REPO UNIT ##########

# == ALL HASHTAGS ================

def test_get_all_hashtags(db_connection):
    '''
    When we call all, we get all hashtags in our db
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)

    hashtags = repository.all()
    assert hashtags == [
        Hashtag(1, "football"),
        Hashtag(2, "memes"),
        Hashtag(3, "shows")
    ]

# == FIND HASHTAG ================

def test_find_by_id(db_connection):
    '''
    We can find the hashtag by the hashtag_id 
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)

    hashtag = repository.find_by_id(hashtag_id=3)
    assert hashtag == Hashtag(3, "shows")

def test_find_by_title(db_connection):
    '''
    We can find the hashtag_id by a potential hashtag title. If it does not exist, we get None.
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)

    assert repository.find_by_title("Shows") == Hashtag(3, "shows")
    assert repository.find_by_title("baseball") == None

# == CREATE NEW HASHTAG ============

def test_check_if_new_and_valid(db_connection):
    '''
    When we have the user creates a post with a non-empty hashtag entry
    We can check if the hashtag is already in the DB
    If it is not, we add it to hashtags
    We can see it in hashtags.all
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)

    assert repository.check_if_new_and_valid("") == False
    assert repository.check_if_new_and_valid(None) == False
    assert repository.check_if_new_and_valid("shows") == False

def test_create_new_hashtag(db_connection):
    '''
    When we have the user creates a post with a non-empty hashtag entry
    We can check if the hashtag is already in the DB
    If it is not, we add it to hashtags
    We can see it in hashtags.all
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)

    assert repository.create(new_tag="Baseball") == 4
    assert repository.all() == [
        Hashtag(1, "football"),
        Hashtag(2, "memes"),
        Hashtag(3, "shows"),
        Hashtag(4, "baseball")
    ]

# == DELETE A HASHTAG ===============

def test_delete_hashtag(db_connection):
    '''
    When we delete a hashtag,
    It should no longer by in all hashtags
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)

    repository.delete(3)
    assert repository.all() == [
        Hashtag(1, "football"),
        Hashtag(2, "memes")
    ]

def test_delete_hashtag_effect_on_post(db_connection):
    '''
    When we delete a hashtag,
    It should be removed from posts that had this hashtag
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)

    assert repository.all_for_post(1) == [
        Hashtag(1, "football"),
        Hashtag(3, "shows")
    ]
    repository.delete(3)
    assert repository.all_for_post(1) == [
        Hashtag(1, "football")
    ]


##############################################

## HASHTAG REPO / POST REPO INTEGRATION ##########

# All hashtags for a post
def test_all_hashtags_for_post(db_connection):
    '''
    We can find a list of all hashtags for a post
    '''
    '''
    If there are no hashtags for the post, we should see "" or None
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)
    assert repository.all_for_post(post_id=1) == [
        Hashtag(1, "football"),
        Hashtag(3, "shows")
    ]
    repository.delete(2)
    assert repository.all_for_post(post_id=3) == []


# Add hashtag to post --- MOVE TO POSTS?
def test_add_hashtag_to_post(db_connection):
    '''
    When we add a hashtag to a post
    We see it in all_hashtags_for_post()
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)
    repository.add_to_post(hashtag_id=2, post_id=1)
    assert repository.all_for_post(1) == [
        Hashtag(1, "football"),
        Hashtag(2, "memes"),
        Hashtag(3, "shows")
    ]

# Delete hashtag from post
def test_delete_hashtag_to_post(db_connection):
    '''
    When we delete a hashtag from a post
    We no longer see it in all_hashtags_for_post()
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = HashtagRepository(db_connection)
    repository.delete_from_post(hashtag_id=1, post_id=1)
    assert repository.all_for_post(1) == [
        Hashtag(3, "shows")
    ]
