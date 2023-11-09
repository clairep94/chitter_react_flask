-- The job of this file is to reset all of our important database tables.
-- And add any data that is needed for the tests to run.
-- This is so that our tests, and application, are always operating from a fresh
-- database state, and that tests don't interfere with each other.

-- First, we must delete (drop) all our tables --------------

-- Join tables
-- When a user adds hashtags to a post, insert into tag_id, post_id (hashtags.id, posts.id)
DROP TABLE IF EXISTS hashtags_posts; -- id, tag_id, post_id
DROP SEQUENCE IF EXISTS hashtags_posts_id_sequence;

-- When a user likes a post, insert into user_id, post_id (user.id, post.id)
-- When a user likes a comment, insert into user_id, comment_id (user.id, comment.id)
DROP TABLE IF EXISTS likes; -- id, user_id, post_id (nullable), comment_id (nullable). (users-posts and users-comments one-many)
DROP SEQUENCE IF EXISTS likes_id_seq;

-- When a userA follows userB, insert into follower_id, followee_id (userA.id, userB.id)
DROP TABLE IF EXISTS follows; -- id, follower_id, followee_id (users-users many to many)
DROP SEQUENCE IF EXISTS follows_id_seq;


DROP TABLE IF EXISTS hashtags;
DROP SEQUENCE IF EXISTS hashtags_id_seq;

DROP TABLE IF EXISTS comments;
DROP SEQUENCE IF EXISTS comments_id_seq; 

DROP TABLE IF EXISTS posts; 
DROP SEQUENCE IF EXISTS posts_id_seq;

DROP TABLE IF EXISTS users; 
DROP SEQUENCE IF EXISTS users_id_seq;




-- Then, we recreate them --------------------------
CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255),
    handle VARCHAR(255),
    name VARCHAR(255),
    joined_on TIMESTAMP
);

CREATE SEQUENCE IF NOT EXISTS posts_id_seq;
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    content VARCHAR(255),
    created_on TIMESTAMP
    -- CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE SEQUENCE IF NOT EXISTS comments_id_seq;
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    post_id INTEGER,
    content VARCHAR(255),
    created_on TIMESTAMP
    -- CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    -- CONSTRAINT fk_posts FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

CREATE SEQUENCE IF NOT EXISTS hashtags_id_seq;
CREATE TABLE hashtags (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255)
);

-- Join tables
CREATE SEQUENCE IF NOT EXISTS follows_id_seq;
CREATE TABLE follows (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER,
    followee_id INTEGER
    -- CONSTRAINT fk_users FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
    -- CONSTRAINT fk_users FOREIGN KEY (followee_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE SEQUENCE IF NOT EXISTS likes_id_seq;
CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    post_id INTEGER NULL, -- can be blank
    comment_id INTEGER NULL -- can be blank
    -- CONSTRAINT fk_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    -- CONSTRAINT fk_posts FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    -- CONSTRAINT fk_comments FOREIGN KEY (comment_id) REFERENCES comments(id) ON DELETE CASCADE
);

CREATE SEQUENCE IF NOT EXISTS hashtags_posts_id_sequence;
CREATE TABLE hashtags_posts (
    id SERIAL PRIMARY KEY,
    hashtag_id INTEGER,
    post_id INTEGER
    -- CONSTRAINT fk_hashtag FOREIGN KEY (hashtag_id) REFERENCES hashtags(id) ON DELETE CASCADE,
    -- CONSTRAINT fk_posts FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);


-- Then we inject some test data: ------------

-- CREATING USERS:
-- Creating 3 test users
INSERT INTO users (email, password, handle, name, joined_on) VALUES ('fifa_email@gmail.com', 'davidBeckam00@', 'FIFAcom', 'FIFA', '2015-07-28');
INSERT INTO users (email, password, handle, name, joined_on) VALUES ('bernie_email@gmail.com', 'feeltheBern12#', 'BernieSanders', 'Bernie Sanders', '2013-09-22');
INSERT INTO users (email, password, handle, name, joined_on) VALUES ('aoc_email@gmail.com', '1234567890a0C', 'AOC', 'Alexandria Ocasio-Cortez', '2017-06-01');



-- CREATE HASHTAGS:
-- Creating 3 hashtags
INSERT INTO hashtags (title) VALUES ('football');
INSERT INTO hashtags (title) VALUES ('memes');
INSERT INTO hashtags (title) VALUES ('shows');


-- MAKING POSTS:
-- User 1 makes Post 1 with Hashtag 1 and 3
INSERT INTO posts (user_id, content, created_on) VALUES (1, 'Has anyone seen the new David Beckham series?', '2023-10-16 12:30:00');
INSERT INTO hashtags_posts (hashtag_id, post_id) VALUES (3, 1);
INSERT INTO hashtags_posts (hashtag_id, post_id) VALUES (1, 1);

-- User 1 makes Post 2 with Hashtag 1, 2
INSERT INTO posts (user_id, content, created_on) VALUES (1, '"football" not "soccer", tyvm', '2023-10-17 10:30:00');
INSERT INTO hashtags_posts (hashtag_id, post_id) VALUES (1, 2);
INSERT INTO hashtags_posts (hashtag_id, post_id) VALUES (2, 2);

-- User 2 makes Post 3 with Hashtags 1
INSERT INTO posts (user_id, content, created_on) VALUES (2, 'I am once again asking for your financial support', '2023-10-17 11:09:00');
INSERT INTO hashtags_posts (hashtag_id, post_id) VALUES (2, 3);


-- COMMENTING POSTS:
-- User 2 makes Comment 1 - Post 1
INSERT INTO comments (user_id, post_id, content, created_on) VALUES (2, 1, 'Yes it was sooo good!', '2023-10-16 19:05:00');
-- User 3 makes Comment 2 - Post 1
INSERT INTO comments (user_id, post_id, content, created_on) VALUES (3, 1, 'the scene where david asked posh about her dads car lollll', '2023-10-16 23:15:00');
-- User 3 makes Comment 3 - Post 2
INSERT INTO comments (user_id, post_id, content, created_on) VALUES (3, 2, 'classic', '2023-10-17 13:47:00');


-- LIKING POSTS & COMMENTS:
-- User 3 likes Post 1, 2
INSERT INTO likes (user_id, post_id) VALUES (3, 1);
-- User 2, 3 like Post 2
INSERT INTO likes (user_id, post_id) VALUES (2, 2);
INSERT INTO likes (user_id, post_id) VALUES (3, 2);

-- User 3 likes Post 3
INSERT INTO likes (user_id, post_id) VALUES (3, 3);

-- User 2 likes Comment 3
INSERT INTO likes (user_id, comment_id) VALUES (2, 3);


-- FOLLOWING:
-- User 3 follows User 1 and 2
INSERT INTO follows (follower_id, followee_id) VALUES (3, 1);
INSERT INTO follows (follower_id, followee_id) VALUES (3, 2);

-- User 2 follows User 3
INSERT INTO follows (follower_id, followee_id) VALUES (2, 3);


