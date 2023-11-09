from lib.models.comment import Comment
from datetime import datetime

class CommentRepository:
    def __init__(self, connection):
        self._connection = connection

    def generate_comments(self, rows) -> list:
        comments = []
        for row in rows:
            comment = Comment(row['id'], row['post_id'], row['user_id'], row['content'], row['created_on'])
            comments.append(comment)
        return comments

    def generate_single_comment(self, rows) -> Comment:
        if rows == []:
            return None
        row = rows[0]
        return Comment(row['id'], row['post_id'], row['user_id'], row['content'], row['created_on'])

    # ========= ALL ==================
    # all comments
    def all(self) -> list[Comment]:
        '''
        When we call all, we get all comments in our db
        '''
        query = 'SELECT * FROM comments'

        rows = self._connection.execute(query)
        return self.generate_comments(rows)

    # ========= FIND ===================
    # find a comment by id
    def find_by_id(self, comment_id:int) -> Comment:
        '''
        We can find a comment by its comment_id
        '''
        query = 'SELECT * FROM comments WHERE id=%s'
        params = [comment_id]

        rows = self._connection.execute(query, params)
        return self.generate_single_comment(rows)

    def find_all_for_post(self, post_id:int) -> Comment:
        '''
        We can find all comments for an individual post
        '''
        query = 'SELECT * FROM comments WHERE post_id=%s'
        params = [post_id]

        rows = self._connection.execute(query, params)
        return self.generate_comments(rows)



    # ========= CREATE ====================
    '''
    When we create content, we have to be logged in and the content entry has to be not empty, otherwise we generate errors.
    If we have any hashtags, we separate them into a list
    '''

    # Validity check -- use before create
    def check_content_valid_errors(self, user_id, content) -> bool:
        if user_id == None:
            return "Please log in to create a comment."
        if content == "" or content == None:
            return "Comment content cannot be empty."
        return None

    # Create comment
    def create(self, post_id, user_id, content, created_on=datetime.now()) -> int:
        query = 'INSERT INTO comments (post_id, user_id, content, created_on) VALUES (%s, %s, %s, %s) RETURNING id'
        params = [post_id, user_id, content, created_on]

        rows = self._connection.execute(query, params)
        comment_id = rows[0]['id']
        # TODO Check steps for this when I make the create_comment page.
        return comment_id ## CHANGE TO POST OBJECT?

    
    # =========== DELETE ===================
    # delete comment -- deleting the comment does not destroy the hashtags, but does destroy comments
    
    def delete(self, comment_id:int) -> None:
        '''
        When we delete a comment
        We will no longer see it in all comments
        We will no longer see it in the user's comments
        We will no longer see it in the parent posts' comments
        '''
        self._connection.execute('DELETE FROM comments WHERE id = %s', [comment_id])
        return None

    # ========= SORT ========================
    def sort_by_descending_date(self, comment_list_ascending_date):
        '''
        We can organise a list of comments by descending date
        By default all queries will be by ascending date.
        '''
        return comment_list_ascending_date[::-1]
    


    ## ============================================================================ ##
    ## ======== INTEGRATION ======================================================= ##
    ## ============================================================================ ##

    # ========= USER ======================
    def find_all_by_user(self, user_id):
        '''
        We can find all comments by a user
        '''
        params = [user_id]
        query = 'SELECT * FROM comments WHERE user_id =%s'

        rows = self._connection.execute(query, params)
        return self.generate_comments(rows)


    # ========= POSTS ======================
    # def find_all_comments_for_post(self, post_id) -> list[Comment]:
    #     '''
    #     Return all comments associated with a post
    #     '''
    #     params = [post_id]
    #     query = 'SELECT * FROM comments WHERE post_id =%s'

    #     rows = self._connection.execute(query, params)
    #     return self.generate_comments(rows)


    # ========= LIKES ======================
    # find_all_likes_for_comment(comment_id) --> like_repository

    # sort comments by likes 
    # TODO This currently does not count 0's for no likes. FIX
    def sort_by_likes(self, comment_list, most_popular=True) -> dict: #TODO: figure out output type after trying integration depending on usage.
        '''
        We can organise a list of comments by the number of likes
        '''
        params = [comment.comment_id for comment in comment_list] #[1,2,3]
        params_placeholders = ", ".join(["%s"] * len(params)) #(%s, %s, %s)        

        # Create a join table with comment_id and likes_count where comment_id is in the comment_ids list.
        query = f"SELECT comment_id, COUNT(*) AS likes_count FROM likes WHERE comment_id IN ({params_placeholders}) GROUP BY comment_id"
        rows = self._connection.execute(query, params)

        # Map of id: comment object in comment_list
        id_to_comment_map = {comment.comment_id: comment for comment in comment_list}
        # comment object to num of likes
        ascending_likes = [
            {"comment": id_to_comment_map[row['comment_id']],
            "likes_count": row['likes_count']} for row in rows
        ]
        if most_popular == True:
            return ascending_likes[::-1] #most popular to least popular
        else:
            return ascending_likes #least popular to most popular.



    # ========= ADDITIONAL FIND BY ================= 
    # - TODO ADD LATER AFTER WEBSITE DRAFT IS DONE.
    # # find by content, case sensitive, one string only 
    # def find_by_content(self, search_string:str) -> None or list[Comment]:
    #     '''
    #     When we search for a comment by content
    #     We see a list of all comments with the search string matching part of the content.
    #     '''
    #     rows = self._connection.execute('SELECT * FROM comments WHERE content LIKE %s'[search_string])
    #     comments = []
    #     for row in rows:
    #         comment = Comment(row['id'], row['user_id'], row['content'], row['created_on'])
    #         comments.append(comment)
    #     return comments





