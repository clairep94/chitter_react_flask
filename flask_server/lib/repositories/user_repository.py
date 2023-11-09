from lib.models.user import User
from datetime import datetime

class UserRepository:
    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    def generate_users(self, rows) -> list:
        users = []
        for row in rows:
            user = User(row['id'], row['email'], row['password'], row['handle'], row['name'], row['joined_on'])
            users.append(user)
        return users
    
    def generate_single_user(self, rows) -> User:
        if rows == []:
            return None
        row = rows[0]
        return User(row['id'], row['email'], row['password'], row['handle'], row['name'], row['joined_on'])


    # == ALL USERS =============
    # Retrieve all registered users from db
    def all(self) -> list[User]:
        query = 'SELECT * FROM users'
        rows = self._connection.execute(query)
        return self.generate_users(rows)

    # == FIND SINGLE USER =============

    # Find a single user by id
    def find(self, user_id:int) -> User:
        query = 'SELECT * FROM users WHERE id=%s'
        params = [user_id]

        rows = self._connection.execute(query, params)
        return self.generate_single_user(rows)
    
    # Find a single user_id by username 
    def find_by_handle(self, handle:str) -> User or None:
        query = 'SELECT * FROM users WHERE handle=%s'
        params = [handle]
        rows = self._connection.execute(query, params)
        return self.generate_single_user(rows)

    # == CREATE NEW USER & ERRORS =============

    # Create a new user
    def create(self, email, password, handle, name, joined_on=datetime.now()) -> int:
        #TODO HASHING FOR PASSWORD
        query = 'INSERT INTO users (email, password, handle, name, joined_on) VALUES (%s, %s, %s, %s, %s) RETURNING id'
        params = [email, password, handle, name, joined_on]
        rows = self._connection.execute(query, params)
        user_id = rows[0]['id'] # SQL creates user_id in serial when a new row is inserted
        return user_id

    # Check if new user's desired handle or email have previously been used:
    # Return list of errors to display or empty list
    def check_registration_duplicate(self, handle:str, email:str) -> list:
        print("STARTING CHECK REGISTRATION DUPLICATE")
        errors = []
        same_email_rows = self._connection.execute('SELECT id FROM users WHERE email = %s', [email])
        if same_email_rows != []:
            errors.append("Email is already registered with an account")
        same_handle_rows = self._connection.execute('SELECT id FROM users WHERE handle =%s', [handle])
        if same_handle_rows != []:
            errors.append("Handle is already registered with an account")
        return errors

    # Check that all entries are valid
    # TODO More rules for these -- eg. no spaces or special characters in handle
    def is_valid(self, email:str, password:str, handle:str, name:str) -> list:
        errors = []
        if email == None or email == "":
            errors.append("Email cannot be empty")
        elif "@" not in email: #TODO Refine this!
            errors.append("Invalid email address")

        if password == None or password == "":
            errors.append("Password cannot be empty")
        elif len(password) <= 8:
            errors.append("Password must be 8 chars or longer")
        # TODO: Add additional rules for password such as needing one num, one special char, one lowercase letter, one upper case letter

        if handle == None or handle == "":
            errors.append("Handle cannot be empty")
        if name == None or name == "":
            errors.append("Name cannot be empty")
        return errors

    # Create printable errors string
    def generate_errors(self, duplicates_errors, validity_errors) -> None or str:
        if duplicates_errors == [] and validity_errors == []:
            return None
        all_errors = duplicates_errors + validity_errors
        return ", ".join(all_errors)


    # == DELETE A USER =============

    # Delete a user by id
    def delete(self, user_id) -> None:
        query = 'DELETE FROM users WHERE id = %s'
        params = [user_id]
        self._connection.execute(query, params)
        return None
    

    ######################################

    ## == INTEGRATION ===================

    # === FOLLOW ========================
    # Find all users who follow this user
    def find_all_followers_of_user(self, user_id):
        query = 'SELECT users.id, users.email, users.password, users.handle, users.name, users.joined_on FROM users JOIN follows ON users.id = follows.follower_id WHERE follows.followee_id =%s'
        params = [user_id]
        rows = self._connection.execute(query, params)
        return self.generate_users(rows)

    # Find number of users who follow this user
    # Check edgecase for 0 followers
    def find_num_followers_of_user(self, user_id):
        return len(self.find_all_followers_of_user(user_id))

    # Find all users this user follows
    def find_all_follows_by_user(self, user_id):
        query = 'SELECT users.id, users.email, users.password, users.handle, users.name, users.joined_on FROM users JOIN follows ON users.id = follows.followee_id WHERE follows.follower_id =%s'
        params = [user_id]
        rows = self._connection.execute(query, params)
        return self.generate_users(rows)

    # Find number of users this user follows
    # Check edgecase for 0 followers
    def find_num_follows_by_user(self, user_id):
        return len(self.find_all_follows_by_user(user_id))

    # === LIKES =========================

    # Find all users who like this post 
    def find_who_liked_post(self, post_id):
        query = 'SELECT users.id, users.email, users.password, users.handle, users.name, users.joined_on FROM users JOIN likes on users.id = likes.user_id WHERE post_id =%s'
        params = [post_id]
        rows = self._connection.execute(query,params)
        return self.generate_users(rows)

    # Find all users who like this comment
    def find_who_liked_comment(self, comment_id):
        query = 'SELECT users.id, users.email, users.password, users.handle, users.name, users.joined_on FROM users JOIN likes on users.id = likes.user_id WHERE comment_id =%s'
        params = [comment_id]
        rows = self._connection.execute(query,params)
        return self.generate_users(rows)

