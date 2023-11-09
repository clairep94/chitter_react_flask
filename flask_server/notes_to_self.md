# Notes for Refactoring & Caching:

Currently storing all methods where the output is a list of that object class.
eg. get_all_likes_for_post is in LikeRepository, not PostRepository.
Storing in the 'many' end of the relationship

Currently prioritising minimising number of SQL queries -- will change to code-readability and code-refactoring if advised

## REFACTORING:

Future fork -- refactor post & comment to inherit from UserContent; refactor like & follow to inheriy from UserEvent

### FOR POST & COMMENT -- UserContent class;

```python
class UserContent:
    def __init__(self, post_id, user_id, created_on, content):
        self.post_id = post_id
        self.user_id = user_id
        self.created_on = created_on
        self.content = content
    
class PostModel(UserContentModel):
    def __init__(self, post_id, user_id, created_on, content):
        super().__init__(post_id, user_id, created_on, content)
    
    def __eq__(self, other):
        if not isinstance(other, Post):
            return False

    def __repr__(self):
        return f"Post({self.post_id}, User #{self.user_id} created Post #{self.post_id} on {self.created_on})"    


class CommentModel(UserContentModel):
    def __init__(self, comment_id, post_id, user_id, created_on, content):
        super().__init__(post_id, user_id, created_on, content)
        self.comment_id = comment_id
    
    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False

    def __repr__(self):
        return f"Comment({self.comment_id}, User #{self.user_id} commented on Post #{self.post_id} on {self.created_on})"    
```

```python
import UserContent

class UserContentRepository:
    def __init__(self, db_connection, table_name, table_columns, UserContent):
        self.db_connection = db_connection
        self.table_name = table_name
        self.table_columns = table_columns
        self.model_class = UserContent
        self.model_class_params = tuple(row[column] for column in table_columns)

    def generate_models(self, rows) -> list:
        models = []
        for row in rows:
            model = self.model_class(self.model_class_params) #can I do this??
            models.append(model)
        return models
    
    def generate_single_model(self, rows) -> self.model_class #can I do this??
        if rows = []:
            return None
        row = rows[0]
        return self.model_class(self.model_class_params) #can I do this??

    #----------------------------------------------#

    def all(self) -> list:
        query = f'SELECT * FROM {self.table_name}'
        rows = self._connection.execute(query)
        return self.generate_posts(rows)

    def find_by_id(self, model_id):
        query = f'SELECT * FROM {self.table_name} WHERE id=%s'
        params = [model_id]
        rows = self._connection.execute(query, params)
        return self.generate_single_model(self, rows)
    
    def check_content_valid_errors(self, user_id, content) -> bool:
        if user_id == None:
            return "Please log in to create a post."
        if content == "" or content == None:
            return "Post content cannot be empty."
        return None

    def delete(self, id):
        query = f'DELETE FROM {self.table_name} WHERE id = %s', [id]
        self._connection.execute(query, param)
        return None
    
    def sort_by_descending_date(self, list_of_models):
        return list_of_models[::-1]
    
    def find_all_by_user(self, user_id):
        params = [user_id]
        query = f'SELECT * FROM {self.table_name} WHERE user_id =%s'

        rows = self._connection.execute(query, params)
        return self.generate_posts(rows)


######################################

class PostRepository(BaseRepository):
    def __init__(self, db_connection):
        super().__init__(db_connection, 'posts', ['id', 'user_id', 'content', 'created_on'], Post)

    # find posts with matching hashtag
    def find_by_hashtag(self, hashtag:str) -> list[Post]: #posts or empty list.
        hashtag = hashtag.lower()
        query = 'SELECT p.id, p.user_id, p.content, p.created_on FROM posts p JOIN hashtags_posts hp ON p.id = hp.post_id JOIN hashtags h ON hp.hashtag_id = h.id WHERE h.title = %s'
        params = [hashtag]

        rows = self._connection.execute(query, params)
        return self.generate_posts(rows)
    
    def create(self, user_id, content, created_on=datetime.now()) -> int: #figure out how to combine
        query = 'INSERT INTO posts (user_id, content, created_on) VALUES (%s, %s, %s) RETURNING id'
        params = [user_id, content, created_on]

        rows = self._connection.execute(query, params)
        id = rows[0]['id']
        return id 
    
    def sort_by_likes(self, post_list, most_popular=True) -> dict: # figure out how to combine
        params = [post.post_id for post in post_list] #[1,2,3]
        params_placeholders = ", ".join(["%s"] * len(params)) #(%s, %s, %s)        

        query = f"SELECT post_id, COUNT(*) AS likes_count FROM likes WHERE post_id IN ({params_placeholders}) GROUP BY post_id"
        rows = self._connection.execute(query, params)

        # Map of id: post object in post_list
        id_to_post_map = {post.post_id: post for post in post_list}
        # post object to num of likes
        ascending_likes = [
            {"post": id_to_post_map[row['post_id']],
            "likes_count": row['likes_count']} for row in rows
        ]
        if most_popular == True:
            return ascending_likes[::-1] #most popular to least popular
        else:
            return ascending_likes #least popular to most popular.


class CommentRepository(BaseRepository):
    def __init__(self, db_connection):
        super().__init__(db_connection, 'comments', ['id', 'post_id', 'user_id', 'content', 'created_on'], Comment)
    
    def create(self, post_id, user_id, content, created_on=datetime.now()) -> int:
        query = 'INSERT INTO comments (post_id, user_id, content, created_on) VALUES (%s, %s, %s, %s) RETURNING id'
        params = [post_id, content, created_on]

        rows = self._connection.execute(query, params)
        id = rows[0]['id']
        return id 

    def find_all_for_post(post_id):
        pass

    def sort_by_likes(self, post_list, most_popular=True) -> dict: # figure out how to combine
        params = [post.post_id for post in post_list] #[1,2,3]
        params_placeholders = ", ".join(["%s"] * len(params)) #(%s, %s, %s)        

        query = f"SELECT post_id, COUNT(*) AS likes_count FROM likes WHERE post_id IN ({params_placeholders}) GROUP BY post_id"
        rows = self._connection.execute(query, params)

        # Map of id: post object in post_list
        id_to_post_map = {post.post_id: post for post in post_list}
        # post object to num of likes
        ascending_likes = [
            {"post": id_to_post_map[row['post_id']],
            "likes_count": row['likes_count']} for row in rows
        ]
        if most_popular == True:
            return ascending_likes[::-1] #most popular to least popular
        else:
            return ascending_likes #least popular to most popular.




    # ========= COMMENTS ======================
    # find_all_comments_for_post(post_id) --> comment_repository


```

### FOR LIKE & FOLLOW -- UserEvent class:

```python
class BaseRepository:
    def __init__(self, connection, table_name):
        self._connection = connection
        self._table_name = table_name

    def create(self, **kwargs) -> int:
        # Construct the query template with placeholders
        query_template = f"INSERT INTO {self._table_name} ({', '.join(kwargs.keys())}) VALUES ({', '.join(['%s'] * len(kwargs))}) RETURNING id"
        
        # Execute the query with the provided keyword arguments
        rows = self._connection.execute(query_template, list(kwargs.values()))
        
        # Retrieve and return the newly created event_id
        return rows[0]['id']

class LikeRepository(BaseRepository):
    def like(self, user_id, post_id=None, comment_id=None) -> int:
        # Call the create method from the base class, passing in the specific keyword arguments
        return self.create(user_id=user_id, post_id=post_id, comment_id=comment_id)

class FollowRepository(BaseRepository):
    def follow(self, follower_id, followee_id) -> int:
        # Call the create method from the base class, passing in the specific keyword arguments
        return self.create(follower_id=follower_id, followee_id=followee_id)
```

## CACHING

Every time something is searched --> store in cache
When new get request is made:
- check cache first
- If none, then retrieve from DB and write to cache
- If yes, then retrieve from cache

Everything something is created --> update cache if in cache

Cache timeout every _____ amount of time? or drop longest ago item after ____ items?

```python
from flask import Flask, render_template
from flask_caching import Cache
from datetime import datetime, timedelta

app = Flask(__name)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Simulated database and data
class Post:
    def __init__(self, id, title):
        self.id = id
        self.title = title

class Comment:
    def __init__(self, id, post_id, text):
        self.id = id
        self.post_id = post_id
        self.text = text

posts = {
    1: Post(1, "Sample Post")
}

comments = {
    1: [Comment(1, 1, "Comment 1"), Comment(2, 1, "Comment 2")]
}

@app.route('/post/<int:post_id>/comments')
def get_comments(post_id):
    post = posts.get(post_id)
    if not post:
        return "Post not found", 404

    # Check if comments are in the cache
    cached_comments = cache.get(f'comments_post_{post_id}')
    if cached_comments is None:
        # If not in cache, fetch from the database
        comments_for_post = comments.get(post_id, [])
        # Store in the cache with no explicit timeout
        cache.set(f'comments_post_{post_id}', comments_for_post)

    return render_template('comments.html', comments=cached_comments)

# Simulated addition of new comments
@app.route('/add_comment/<int:post_id>/<text>')
def add_comment(post_id, text):
    new_comment = Comment(len(comments.get(post_id, []), post_id, text)
    comments[post_id].append(new_comment)
    
    # Update the cache when a new comment is added
    cache.set(f'comments_post_{post_id}', comments[post_id])
    
    return f"Added new comment: {text}"

if __name__ == '__main__':
    app.run()

```
