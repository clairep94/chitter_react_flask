from playwright.sync_api import Page, expect

# Tests for your routes go here

# == Homepage == chwitter.com/ ==
'''
When we go to the homepage
We should see the following text:

Y
Happening now
Join today.

[Create Account]<a href="/sign_up">

Already have an account?  
[Sign in] <a href="/sign_in">
'''
def test_landingpage(page, test_web_address):
    page.goto(f"http://{test_web_address}/")
    
    #Page headers
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Y")
    h2_tag = page.locator("h2")
    expect(h2_tag).to_have_text("Happening now")
    h3_tag = page.locator("h3")
    expect(h3_tag).to_have_text("Join today.")
    h4_tag = page.locator("h4")
    expect(h4_tag).to_have_text("Already have an account?")
    
    anchor_tag = page.locator("a")
    expect(anchor_tag).to_have_text([
        "Create Account",
        "Sign in"
    ])



# == ALL TWEETS, NO LOGIN == chwitter.com/home ==
'''
When we go to all tweets
We should see:
- Y Logo in H1
- link for the /home
- link for New Post
- link for Your Account
- button for Sign out

- A list of all posts in order of posting where earliest is first
- For each post:
    - Name (bold) @Username (italic) - Xh ago or Xdays ago or date
    - Content
    - Upvotes
    - button for upvote/downvoting
'''
def test_homepage(page, test_web_address):
    page.goto(f"http://{test_web_address}/home")

    #Page headers
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Y")
    anchor_tag = page.locator("a")
    expect(anchor_tag).to_have_text([
        "Home",
        "New Post",
        "Your Account",
        "Sign Out"
    ])

    #List of posts



# == TWEET == chwitter.com/posts/<id> ==
'''
When we go to a single tweet
We should see:
- Y Logo in H1
- link for the /home
- link for New Post
- link for Your Account
- button for Sign out

<b>{Name}</b> @{Username} - {hours ago or date}h
{content}
{upvotes}

- button for delete
'''
def test_single_tweet(page, test_web_address):
    page.goto(f"http://{test_web_address}/posts/<id>")

    #Page headers
    h1_tag = page.locator("h1")
    expect(h1_tag).to_have_text("Y")
    anchor_tag = page.locator("a")
    expect(anchor_tag).to_have_text([
        "Home",
        "New Post",
        "Your Account",
        "Sign Out"
    ])

    #Single Post











# === Example Code Below ===

"""
We can get an emoji from the /emoji page
"""
def test_get_emoji(page, test_web_address): # Note new parameters
    # We load a virtual browser and navigate to the /emoji page
    page.goto(f"http://{test_web_address}/emoji")

    # We look at the <strong> tag
    strong_tag = page.locator("strong")

    # We assert that it has the text ":)"
    expect(strong_tag).to_have_text(":)")

# === End Example Code ===
