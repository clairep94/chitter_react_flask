from lib.repositories.user_repository import User, UserRepository
from datetime import datetime

## USER CLASS ####

def test_user_eq():
    user1 = User(1, "test_email@gmail.com", "this9ISaSTRONGp@@@Sword", "testUser99", "John Doe", datetime(2023, 10, 21))
    user2 = User(1, "test_email@gmail.com", "this9ISaSTRONGp@@@Sword", "testUser99", "John Doe", datetime(2023, 10, 21))
    assert user1 == user2

def test_user_repr():
    user1 = User(1, "test_email@gmail.com", "this9ISaSTRONGp@@@Sword", "testUser99", "John Doe", datetime(2023, 10, 21))
    assert str(user1) == "User(1, Display Name: John Doe, Handle: @testUser99)"

##############################################

## USER REPOSITORY ###########

# ==== ALL =========== #######
def test_all(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.all() == [
        User(1, "fifa_email@gmail.com", "davidBeckam00@", "FIFAcom", "FIFA", datetime(2015,7,28)),
        User(2, "bernie_email@gmail.com", "feeltheBern12#", "BernieSanders", "Bernie Sanders", datetime(2013, 9, 22)),
        User(3, "aoc_email@gmail.com", "1234567890a0C", "AOC", "Alexandria Ocasio-Cortez", datetime(2017, 6, 1))
    ]

# ====== FIND ========== #
def test_find(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.find(3) == User(3, "aoc_email@gmail.com", "1234567890a0C", "AOC", "Alexandria Ocasio-Cortez", datetime(2017, 6, 1))
    assert repository.find(5) == None

def test_find_by_handle(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.find_by_handle("AOC") == User(3, "aoc_email@gmail.com", "1234567890a0C", "AOC", "Alexandria Ocasio-Cortez", datetime(2017, 6, 1))
    assert repository.find_by_handle("NotAnAccount") == None

# ======= CREATE ======= #
def test_create(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.create("test_email@gmail.com", "this9ISaSTRONGp@@@Sword", "testUser99", "John Doe", datetime(2023, 10, 21)) == 4
    assert repository.all() == [
        User(1, "fifa_email@gmail.com", "davidBeckam00@", "FIFAcom", "FIFA", datetime(2015,7,28)),
        User(2, "bernie_email@gmail.com", "feeltheBern12#", "BernieSanders", "Bernie Sanders", datetime(2013, 9, 22)),
        User(3, "aoc_email@gmail.com", "1234567890a0C", "AOC", "Alexandria Ocasio-Cortez", datetime(2017, 6, 1)),
        User(4, "test_email@gmail.com", "this9ISaSTRONGp@@@Sword", "testUser99", "John Doe", datetime(2023, 10, 21))
    ]

# ------- FORM CHECK ERRORS FOR CREATE -------------- #
def test_check_registration_duplicate(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.check_registration_duplicate("AOC", "notarepeatemail@gmail.com") == ["Handle is already registered with an account"]
    assert repository.check_registration_duplicate("SomeHandle", "bernie_email@gmail.com") == ["Email is already registered with an account"]
    assert repository.check_registration_duplicate("AOC", "aoc_email@gmail.com") == ["Email is already registered with an account", "Handle is already registered with an account"]

def test_is_valid(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.is_valid("", "", "", "") == ["Email cannot be empty", "Password cannot be empty", "Handle cannot be empty", "Name cannot be empty"]
    assert repository.is_valid("notavalidemail", "pw2short", "Handle", "Name") == ["Invalid email address", "Password must be 8 chars or longer"]

def test_generate_errors(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.generate_errors([], []) == None
    assert repository.generate_errors([], ["Invalid email address", "Password must be 8 chars or longer"]) == "Invalid email address, Password must be 8 chars or longer"
    assert repository.generate_errors(["Email is already registered with an account"], ["Invalid email address", "Password must be 8 chars or longer"]) == "Email is already registered with an account, Invalid email address, Password must be 8 chars or longer"

## FOLLOW INTEGRATION

def test_find_all_followers(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.find_all_followers_of_user(1) == [User(3, "aoc_email@gmail.com", "1234567890a0C", "AOC", "Alexandria Ocasio-Cortez", datetime(2017, 6, 1))]
    repository.create("test_email@gmail.com", "this9ISaSTRONGp@@@Sword", "testUser99", "John Doe", datetime(2023, 10, 21))
    assert repository.find_all_followers_of_user(4) == []
    assert repository.find_num_followers_of_user(1) == 1
    assert repository.find_num_followers_of_user(4) == 0


def test_find_all_follows(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.find_all_follows_by_user(1) == []
    assert repository.find_num_follows_by_user(1) == 0
    assert repository.find_all_followers_of_user(1) == [User(3, "aoc_email@gmail.com", "1234567890a0C", "AOC", "Alexandria Ocasio-Cortez", datetime(2017, 6, 1))]
    assert repository.find_num_followers_of_user(1) == 1

## LIKE INTEGRATION

def test_find_who_liked_post(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.find_who_liked_post(1) == [User(3, "aoc_email@gmail.com", "1234567890a0C", "AOC", "Alexandria Ocasio-Cortez", datetime(2017, 6, 1))]
    assert repository.find_who_liked_post(2) == [
        User(2, "bernie_email@gmail.com", "feeltheBern12#", "BernieSanders", "Bernie Sanders", datetime(2013, 9, 22)),        
        User(3, "aoc_email@gmail.com", "1234567890a0C", "AOC", "Alexandria Ocasio-Cortez", datetime(2017, 6, 1))
        ]
    
def test_find_who_liked_comment(db_connection):
    db_connection.seed("seeds/chwitter.sql")
    repository = UserRepository(db_connection)

    assert repository.find_who_liked_comment(1) == []
    assert repository.find_who_liked_comment(3) == [User(2, "bernie_email@gmail.com", "feeltheBern12#", "BernieSanders", "Bernie Sanders", datetime(2013, 9, 22))]
