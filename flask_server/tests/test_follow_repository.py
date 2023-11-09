from lib.models.follow import Follow
from lib.repositories.follow_repository import FollowRepository, User
from lib.repositories.user_repository import UserRepository
from datetime import datetime

## FOLLOW CLASS ###

def test_follow_eq():
    event1 = Follow(1, 1, 2)
    event2 = Follow(1, 1, 2)
    assert event1 == event2

def test_follow_repr():
    event1 = Follow(1, 1, 2)
    assert str(event1) == "Follow(1, User #1 followed User #2)"

##############################################

## FOLLOW REPO UNIT ##########

def test_get_all_follow_events(db_connection):
    '''
    When we call all, we get all follow events in our db
    '''
    # Probably won't use this on our website
    db_connection.seed("seeds/chwitter.sql")
    repository = FollowRepository(db_connection)

    follow_events = repository.all()
    assert follow_events == [
        Follow(1, 3, 1),
        Follow(2, 3, 2),
        Follow(3, 2, 3)
    ]

def test_find_event_by_id(db_connection):
    '''
    We can find a follow event by the follow_event_id
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = FollowRepository(db_connection)

    follow_event = repository.find_event_by_id(1)
    assert follow_event == Follow(1, 3, 1)

def test_find_event_by_users(db_connection):
    '''
    We can find the id of the follow event between two users.
    If the event does not exist, we get None.
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = FollowRepository(db_connection)

    follow_event = repository.find_event_by_users(1, 3)
    assert follow_event == None
    follow_event = repository.find_event_by_users(3, 1)
    assert follow_event == 1


def test_check_if_already_following(db_connection):
    '''
    If the follower user is already following the desired followee, we get True (already following.) Otherwise we get False (not yet following).
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = FollowRepository(db_connection)

    # users are not already following eachother
    follow_event = repository.find_event_by_users(1, 3)
    assert follow_event == None
    assert repository.check_if_already_following(1, 3) == False

    # users are already following eachother
    follow_event = repository.find_event_by_users(3, 1)
    assert follow_event == 1
    assert repository.check_if_already_following(3, 1) == True

def test_check_if_valid(db_connection):
    '''
    Users cannot like their own profile.
    When we check if valid against two identical user ids, we get False
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = FollowRepository(db_connection)

    assert repository.check_if_valid(1, 3) == True
    assert repository.check_if_valid(1, 1) == False

def test_follow(db_connection):
    '''
    When one user follows another, we create a follow event.
    When we call #all, we can see the new follow event in the list of events.
    '''
    # TODO when we delete a user, we no longer see the user among their follow's followers
    db_connection.seed("seeds/chwitter.sql")
    repository = FollowRepository(db_connection)

    assert repository.follow(1, 3) == 4
    assert repository.all() == [
        Follow(1, 3, 1),
        Follow(2, 3, 2),
        Follow(3, 2, 3),
        Follow(4, 1, 3)
    ]
    user_repository = UserRepository(db_connection)
    assert user_repository.find_all_followers_of_user(3) == [
        User(2, "bernie_email@gmail.com", "feeltheBern12#", "BernieSanders", "Bernie Sanders", datetime(2013, 9, 22)),
        User(1, "fifa_email@gmail.com", "davidBeckam00@", "FIFAcom", "FIFA", datetime(2015,7,28))
        ]
    assert user_repository.find_all_follows_by_user(1) == [User(3, "aoc_email@gmail.com", "1234567890a0C", "AOC", "Alexandria Ocasio-Cortez", datetime(2017, 6, 1))]

def test_unfollow(db_connection):
    '''
    When one user unfollows another, we delete the follow event
    When we call #all, we can see the event has been deleted in the list of events.
    '''
    db_connection.seed("seeds/chwitter.sql")
    repository = FollowRepository(db_connection)

    repository.unfollow(3, 2)
    assert repository.all() == [
        Follow(1, 3, 1),
        Follow(3, 2, 3)
    ]
    user_repository = UserRepository(db_connection)
    assert user_repository.find_all_followers_of_user(2) == []
    assert user_repository.find_all_follows_by_user(3) == [User(1, "fifa_email@gmail.com", "davidBeckam00@", "FIFAcom", "FIFA", datetime(2015,7,28))]