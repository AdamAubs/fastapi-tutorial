from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# first app object
# include post.router; goes into the router folder then post file and looks for the the routes in their
app.include_router(post.router)
# same idea here. Grabs router object from user file allowing to import all of the specific routes
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to my api!!!!"}


""

# Types
# Declaring type hints as function parameters
# def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
# return item_a, item_b, item_c, item_d, item_e

# Generic types with type parameters
# items_t is a tuple with 3 items, an 2 int's and a str
# items_s is a set, and each of its items is of type bytes
# def proccess_items(items_t: tuple[int, int, str], items_s: set[bytes]):
# return items_t, items_s

# To define a dict you pass two parameters, seperated by commas
# The first type of parameter is for the keys of the dict
# The second type is for the values of the dict
# prices is a dict: keys are of type str and values are of type float
# def process_items(prices: dict[str, float]):
# for item_name, item_price in prices.items():
#     print(item_name)
#     print(item_price)
# my_posts = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "favorite foods", "content": "I like pizza", "id": 2},
# ]


# # finds post with passed id
# def find_post(id):
#     # loops through my_post list
#     for p in my_posts:
#         # check to see if passed id matches any id in my_posts dict
#         if p["id"] == id:
#             return p


# # finds the index of the id passed
# def find_index_post(id):
#     # loops through my_post list using the enumerate function which gets the post and index of the post in the list
#     for i, p in enumerate(my_posts):
#         # if the post matches the passed id return the index of that post
#         if p["id"] == id:
#             return i

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     # posts = db.query(models.Post)
#     # print(posts)
#     # under the hood sqlalechemy query object above "db.query(models.Post)" is turning the sql query
#     # into python syntax
#     # Output: SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published
#     # FROM posts
#     # However to run the query we need to run a specific method
#     posts = db.query(models.Post).all()

#     return {"data": "success"}
