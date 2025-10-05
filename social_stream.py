#!/usr/bin/env python3
# SocialStream MongoDB Lab - Starter Code

from bson import ObjectId

##########################################################################

# Part 2: MongoDB Setup

# TODO:
# Step 1: Establish a Connection
# Step 2: Select/Create a Database
# Step 3: Define Collection Objects
# Step 4: (Optional) Test the Connection
print("Selected DB:", db.name)
print("Initial collections:", db.list_collection_names())

# If data exists in collections, delete it. Makes it easier for testing. Comment out if required.
users_col.delete_many({})
posts_col.delete_many({})
comments_col.delete_many({})


##########################################################################

# Part 3: CRUD Operations

# Step 5: CREATE - Inserting Documents
# Define some sample users
sample_users = [
    # TODO: populate with at least 5 user dicts, e.g. {"username": "alice", "name": "Alice ...", "email": "..."}
]
result = users_col.insert_many(sample_users)
print(f"Inserted {len(result.inserted_ids)} users. IDs: {result.inserted_ids}")

# Maybe fetch and print all users to verify
for user in users_col.find({}):
    print("User:", user)


# Insert sample posts
# First, get some user IDs for reference
# e.g., alice_id = users_col.find_one({"username": "alice"})["_id"]
# TODO: retrieve user IDs needed for posts
# Define sample_posts list with user_id, content, timestamp, likes fields
sample_posts = [
    # TODO: create a few post dicts
    # {"user_id": alice_id, "content": "Hello, this is my first post!", "timestamp": "2025-10-02T12:00:00", "likes": 0},
    # ... more posts by other users
]
result = posts_col.insert_many(sample_posts)
print(f"Inserted {len(result.inserted_ids)} posts.")

# Verify posts insertion
for post in posts_col.find({}):
    print("Post:", post)


# Insert sample comments

# Store post IDs for later use
post_ids = list(result.inserted_ids)
# With this, you can access post id of the posts using indexes - post_ids[0], post_ids[1], post_ids[2]

print("\nVerifying posts (showing first 3):")
for i, post in enumerate(posts_col.find({}).limit(3)):
    author = users_col.find_one({"_id": post["user_id"]})
    print(f"  - {author['username']}: \"{post['content'][:40]}...\" (Likes: {post['likes']})")

sample_comments = [
    # TODO: create comment dicts with post_id and user_id references
    # {"post_id": post_ids[0], "user_id": bob_id, "text": "Nice post!", "timestamp": "2025-10-02T13:30:00"},
    # ... more comments
]
result = comments_col.insert_many(sample_comments)
print(f"Inserted {len(result.inserted_ids)} comments.")

# Verify comments
for comment in comments_col.find({}):
    print("Comment:", comment)

# Step 6: READ - Basic Queries to Retrieve Data
# Find one example: find a user by username
user_alice = users_col.find_one({"username": "alice"})
print("Found user alice:", user_alice)
# Find all posts by alice (using alice's _id if available)
if user_alice:
    alice_posts = posts_col.find({"user_id": user_alice["_id"]})
    print("Alice's posts:")
    for p in alice_posts:
        print(p)
# Count comments on a particular post (if we have a post_id)
# TODO: pick a post_id from sample_posts to count comments
# e.g., some_post_id = sample_posts[0]["_id"] or use find_one to get one post
# print(comments_col.count_documents({"post_id": some_post_id}), "comments on post", some_post_id)


# Step 7: UPDATE - Modifying Documents
# Update a user's profile (e.g., Bob's name or add bio)
# TODO: modify user details

# Increment likes on a post
# TODO: pick a post and increment its likes by a certain number
# posts_col.update_one(
# {"_id": some_post_id},# filter by the post's id
# {"$inc": {"likes": 1}}
# )

# Step 8: DELETE - Removing Documents
# Delete a comment (example)
# TODO: pick a comment to delete, e.g., find one comment by content or user
# TODO: pick a comment to delete, e.g., find one comment by content or user
# comments_col.delete_one({"_id": comment_to_delete["_id"]})
# Remeber to check if the comment is has been successfully deleted after executing delete_one

##########################################################################

# Part 3: Queries and Aggregations

# 3.1 Most liked post
# TODO: use find and sort according to the prac description to find the most liked post
# once fetched, print the most liked post. Optionally, get the author's name and print that as well.

# 3.2 Top commenter
# TODO: add aggregration pipeline structure according to the practical description
top_commenter = list(comments_col.aggregate(pipeline))
if top_commenter:
    top = top_commenter[0]
    user_id = top["_id"]
    count = top["count"]
    user_doc = users_col.find_one({"_id": user_id})
    user_name = user_doc["username"] if user_doc else str(user_id)
    print(f"Top commenter: {user_name} with {count} comments.")

##########################################################################

