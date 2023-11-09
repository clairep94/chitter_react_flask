import os
from flask import Flask, request, session, jsonify
from lib.database_connection import get_flask_database_connection


# Create a new Flask app
app = Flask(__name__)


mock_database = [{"event_id":"1","band_name":"The Crooked Spires","image_url":"","description":"The Crooked Spires are a British rock band formed in London in 2022. The band consists of lead vocalist and guitarist Steve Spire, bassist and backing vocalist Dave Spire, drummer and backing vocalist Pete Spire, and keyboard player and backing vocalist Andy Spire.","time":"2023-09-15T20:00:00Z","location":"The O2 Arena, London","favourited":false},{"event_id":"2","band_name":"The Falling Stars","image_url":"","description":"The Falling Stars are an English rock band formed in Liverpool in 2021. The band consists of lead vocalist and guitarist Jack Star, bassist and backing vocalist Jill Star, drummer and backing vocalist Pete Star, and keyboard player and backing vocalist Andy Star.","time":"2023-10-12T21:00:00Z","location":"Wembley Stadium, London","favourited":false},{"event_id":"3","band_name":"The Revolving Doors","image_url":"","description":"The Revolving Doors are an American rock band formed in Las Vegas in 2020. The band consists of lead vocalist and keyboardist Brandon Door, guitarist and backing vocalist Dave Door, bassist and backing vocalist Mark Door, and drummer Ronnie Door.","time":"2023-11-19T20:00:00Z","location":"The SSE Arena, Wembley, London","favourited":false},{"event_id":"4","band_name":"The Shifting Sands","image_url":"","description":"The Shifting Sands are an English rock band formed in Manchester in 2019. The band consists of lead vocalist and guitarist Liam Sand, bassist and backing vocalist Noel Sand, rhythm guitarist and backing vocalist Paul Sand, and drummer Tony Sand.","time":"2023-12-03T21:00:00Z","location":"The Royal Albert Hall, London","favourited":false},{"event_id":"5","band_name":"The Untamed Beasts","image_url":"","description":"The Untamed Beasts are an English rock band formed in Sheffield in 2018. The band consists of lead vocalist and guitarist Alex Beast, guitarist and backing vocalist Jamie Beast, bassist and backing vocalist Nick Beast, and drummer Matt Beast.","time":"2024-01-17T20:00:00Z","location":"The SSE Arena, Wembley, London","favourited":false},{"event_id":"6","band_name":"The Burning Flames","image_url":"","description":"The Burning Flames are an English rock band formed in Abingdon, Oxfordshire in 2017. The band consists of lead vocalist and guitarist Thom Flame, guitarist and keyboards Jonny Flame, bassist and backing vocalist Ed Flame, Colin Flame on bass guitar, and backing vocals, and Philip Flame on drums, percussion.","time":"2024-02-21T21:00:00Z","location":"The O2 Arena, London","favourited":false},{"event_id":"7","band_name":"The Echoing Voices","image_url":"","description":"The Echoing Voices are an English rock band formed in Manchester in 2016. The band consists of lead vocalist, guitarist, and synthesizer Matthew Voice, guitarist and backing vocalist Adam Voice, drummer and keyboards George Voice, and bass guitar and backing vocalist Ross Voice.","time":"2024-03-15T20:00:00Z","location":"The SSE Arena, Wembley, London","favourited":false},{"event_id":"8","band_name":"The Wandering Troubadours","image_url":"","description":"The Wandering Troubadours are a British folk band formed in London in 2022. The band consists of lead vocalist and guitarist Steve Troubadour, bassist and backing vocalist Dave Troubadour, drummer and backing vocalist Pete Troubadour, and keyboard player and backing vocalist Andy Troubadour.","time":"2023-09-22T20:00:00Z","location":"The Roundhouse, London","favourited":false},{"event_id":"9","band_name":"The Rising Storm","image_url":"","description":"The Rising Storm are an English heavy metal band formed in Liverpool in 2021. The band consists of lead vocalist and guitarist Jack Storm, bassist and backing vocalist Jill Storm, drummer and backing vocalist Pete Storm, and keyboard player and backing vocalist Andy Storm.","time":"2023-10-29T21:00:00Z","location":"The Brixton Academy, London","favourited":false},{"event_id":"10","band_name":"The Eternal Flame","image_url":"","description":"The Eternal Flame are an American pop rock band formed in Las Vegas in 2020. The band consists of lead vocalist and keyboardist Brandon Flame, guitarist and backing vocalist Dave Flame, bassist and backing vocalist Mark Flame, and drummer Ronnie Flame.","time":"2023-11-26T20:00:00Z","location":"The SSE Arena, Wembley, London","favourited":false}]

# == Your Routes Here ==


### ===== POSTS ===== ####

# == ALL POSTS == chwitter.com/home ==

@app.route('/posts/all', methods = ['GET'])
def home():
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return mock_database

# == CREATE POST PAGE ==
@app.route('/posts/new', methods = ['GET'])
def create_post_page():
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return "New Post"

# == CREATE POST ==
@app.route('/posts', methods = ['POST'])
def create_post():
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return "Create Post"

# == SHOW POST == chwitter.com/posts/<id> ==
@app.route('/posts/<id>', methods = ['GET'])
def show_post(id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return mock_database[0]

# == DELETE POST == chwitter.com/posts/<id>/delete --> chwitter.com/home ==
@app.route('/posts/<id>/delete', methods = ['POST'])
def delete_post(id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return "Delete Post"

# == UPVOTE/DOWNVOTE POST == page refresh
'''
When we click upvote or downvote, we upvote or downvote a tweet
We will refresh the page and see that the number of upvotes/downvotes has increase by 1.
** We can only upvote/downvote once.
'''
# TODO These only work on the homepage, not on the individual post page.
@app.route('/posts/<id>/upvote', methods = ['POST'])
def upvote_post(id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(request.referrer)

@app.route('/posts/<id>/downvote', methods = ['POST'])
def downvote_post(id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(request.referrer)


### ===== COMMENTS ===== ####

# == SHOW COMMENT == chwitter.com/posts/<post_id>/comments/<id> ==
@app.route('/posts/<post_id>/comments/<id>', methods = ['GET'])
def show_comment(post_id, id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return render_template('show_comment.html', errors=None)

# == DELETE POST == chwitter.com/<post_id>/comments/<id>/delete --> chwitter.com/home ==
@app.route('/posts/<post_id>/comments/<id>/delete', methods = ['POST'])
def delete_comment(post_id, id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(url_for('home')) #return home or parent post


# == UPVOTE/DOWNVOTE COMMENT == page refresh
'''
When we click upvote or downvote, we upvote or downvote a comment
We will refresh the page and see that the number of upvotes/downvotes has increase by 1.
** We can only upvote/downvote once.
'''
# TODO These only work on the homepage, not on the individual post page.
@app.route('/posts/<post_id>/comments/<id>/upvote', methods = ['POST'])
def upvote_comment(post_id, id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(request.referrer) #return home or parent post

@app.route('/posts/<post_id>/comments/<id>/downvote', methods = ['POST'])
def downvote_comment(post_id, id):
    connection = get_flask_database_connection(app)
    # post_repository = PostRepository(connection)
    # post = post_repository.all()
    return redirect(request.referrer) #return home or parent post





### ===== USERS ===== ####

# == USER == chwitter.com/users/<id> ==
'''
When we go to the link for single user, we should see:
We should see:
- Y Logo in H1
- link for the /home
- link for New Post
- link for Your Account

- A list of all posts in order of posting where earliest is first
- For each post:
    - Name (bold) @Username (italic) (link) - Xh ago or Xdays ago or date
    - Content
    - Upvotes
    - button for upvoting/downvoting
'''

# == ALL USERS ==
'''
When we go to the link for single user, we should see:
We should see:
- Y Logo in H1
- link for the /home
- link for New Post
- link for Your Account

- A list of all users. For each user:
    - Name (bold) @Username (italic) (link)

'''

# == CREATE NEW USER == chwitter.com/sign_up==
@app.route('/sign_up', methods = ['GET'])
def sign_up():
    return "<h1>TODO: CREATE SIGN UP PAGE<H1>"


# == SIGN IN == chwitter.com/login ==
@app.route('/login', methods = ['GET'])
def login():
    return "<h1>TODO: CREATE LOGIN PAGE<H1>"


# == SIGN OUT == chwitter.com/logout ==




# == Example Code Below ==

# GET /emoji
# Returns a smiley face in HTML
# Try it:
#   ; open http://localhost:5001/emoji
@app.route('/emoji', methods=['GET'])
def get_emoji():
    # We use `render_template` to send the user the file `emoji.html`
    # But first, it gets processed to look for placeholders like {{ emoji }}
    # These placeholders are replaced with the values we pass in as arguments
    return render_template('emoji.html', emoji=':)')

# This imports some more example routes for you to see how they work
# You can delete these lines if you don't need them.
# from example_routes import apply_example_routes
# apply_example_routes(app)

# == End Example Code ==
from lib.repositories.post_repository import Post, PostRepository


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':

    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))


