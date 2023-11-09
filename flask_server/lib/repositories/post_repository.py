from lib.models.post import Post
from datetime import datetime

class PostRepository:
    def __init__(self, connection):
        self._connection = connection

    def generate_posts(self, rows) -> list:
        posts = []
        for row in rows:
            post = Post(row['id'], row['user_id'], row['content'], row['created_on'])
            posts.append(post)
        return posts

    def generate_single_post(self, rows) -> Post:
        if rows == []:
            return None
        row = rows[0]
        return Post(row['id'], row['user_id'], row['content'], row['created_on'])

    # ========= ALL ==================
    # all posts
    def all(self) -> list[Post]:
        '''
        When we call all, we get all posts in our db
        '''
        query = 'SELECT * FROM posts'

        rows = self._connection.execute(query)
        return self.generate_posts(rows)

    # ========= FIND ===================
    # find a post by id
    def find_by_id(self, post_id:int) -> Post:
        '''
        We can find a post by its post_id
        '''
        query = 'SELECT * FROM posts WHERE id=%s'
        params = [post_id]

        rows = self._connection.execute(query, params)
        return self.generate_single_post(rows)

    # find posts with matching hashtag
    def find_by_hashtag(self, hashtag:str) -> list[Post]: #posts or empty list.
        '''
        We can find a list of all post id's with a certain hashtag
        If the hashtag doesn't exist, we get None
        If no posts are attached to the hashtag, we get None
        '''
        hashtag = hashtag.lower()
        query = 'SELECT p.id, p.user_id, p.content, p.created_on FROM posts p JOIN hashtags_posts hp ON p.id = hp.post_id JOIN hashtags h ON hp.hashtag_id = h.id WHERE h.title = %s'
        params = [hashtag]

        rows = self._connection.execute(query, params)
        return self.generate_posts(rows)

    # ========= CREATE ====================
    '''
    When we create content, we have to be logged in and the content entry has to be not empty, otherwise we generate errors.
    If we have any hashtags, we separate them into a list
    '''

    # Validity check -- use before create
    def check_content_valid_errors(self, user_id, content) -> bool:
        if user_id == None:
            return "Please log in to create a post."
        if content == "" or content == None:
            return "Post content cannot be empty."
        return None

    # Create post
    def create(self, user_id, content, created_on=datetime.now()) -> int:
        query = 'INSERT INTO posts (user_id, content, created_on) VALUES (%s, %s, %s) RETURNING id'
        params = [user_id, content, created_on]

        rows = self._connection.execute(query, params)
        post_id = rows[0]['id']
        # TODO Check steps for this when I make the create_post page.
        return post_id ## CHANGE TO POST OBJECT?

    
    # =========== DELETE ===================
    # delete post -- deleting the post does not destroy the hashtags, but does destroy comments
    
    def delete(self, post_id:int) -> None:
        '''
        When we delete a post
        We will no longer see it in all posts
        We will no longer see it in the user's posts
        ** We will no longer see its comments in all comments 
        ** We will no longer see the comments in their respective poster's comments
        '''
        self._connection.execute('DELETE FROM posts WHERE id = %s', [post_id])
        return None

    # ========= SORT ========================
    def sort_by_descending_date(self, post_list_ascending_date):
        '''
        We can organise a list of posts by descending date
        By default all queries will be by ascending date.
        '''
        return post_list_ascending_date[::-1]
    


    ## ============================================================================ ##
    ## ======== INTEGRATION ======================================================= ##
    ## ============================================================================ ##

    # ========= USER ======================
    def find_all_by_user(self, user_id):
        '''
        We can find all posts by a user
        '''
        params = [user_id]
        query = 'SELECT * FROM posts WHERE user_id =%s'

        rows = self._connection.execute(query, params)
        return self.generate_posts(rows)


    # ========= COMMENTS ======================
    # find_all_comments_for_post(post_id) --> comment_repository

    # ========= HASHTAGS ======================
    def generate_hashtags(self, content):
        '''
        We can search through the content of a post when it is created and generate hashtags -- strings starting with #, separated by whitespace
        '''
        content_list = content.split(" ")
        hashtags_list = [word[1:] for word in content_list if word[0] == "#" and word != "#"]
        return hashtags_list

    # ========= LIKES ======================
    # find_all_likes_for_post(post_id) --> like_repository

    # TODO This currently does not count 0's for no likes. FIX
    # sort posts by likes 
    def sort_by_likes(self, post_list, most_popular=True) -> dict: #TODO: figure out output type after trying integration depending on usage.
        '''
        We can organise a list of posts by the number of likes
        '''
        params = [post.post_id for post in post_list] #[1,2,3]
        params_placeholders = ", ".join(["%s"] * len(params)) #(%s, %s, %s)        

#         view_query = 'CREATE OR REPLACE VIEW PostLikesCount AS like.id as like_id, COALESCE(COUNT(like.id), 0) AS likes_count FROM posts LEFT JOIN likes on post.id = like.post_id GROUP BY post.id'

#         # Create a join table with post_id and likes_count where post_id is in the post_ids list.
#         query = f"SELECT comments.*, COALESCE(CommentLikesCount.likes_count, 0) AS likes_count FROM comments LEFT JOIN CommentLikesCount ON comments.id = CommentLikesCount.comment_id WHERE ;
# "

        # Create a join table with post_id and likes_count where post_id is in the post_ids list.
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

    def unlike(self, event_id) -> None: #copied from Like Repo, just using to test sort_by_likes ability to handle posts with no likes.
        self._connection.execute('DELETE FROM likes WHERE id=%s', [event_id])
        return None


    # ========= ADDITIONAL FIND BY ================= 
    # - TODO ADD LATER AFTER WEBSITE DRAFT IS DONE.
    # # find by content, case sensitive, one string only 
    # def find_by_content(self, search_string:str) -> None or list[Post]:
    #     '''
    #     When we search for a post by content
    #     We see a list of all posts with the search string matching part of the content.
    #     '''
    #     rows = self._connection.execute('SELECT * FROM posts WHERE content LIKE %s'[search_string])
    #     posts = []
    #     for row in rows:
    #         post = Post(row['id'], row['user_id'], row['content'], row['created_on'])
    #         posts.append(post)
    #     return posts





