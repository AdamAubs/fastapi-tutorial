from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List, Annotated
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func


router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_post(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = " ",
):
    print(limit)
    # ***Using RAW SQL with psycopg2 PostgreSQL adapter for python (Low-Level)***
    # # Gets all the posts froms the posts table in the database
    # cursor.execute("""SELECT  * FROM posts """)
    # # Retrieves all the posts that were selected (stores in variable posts)
    # posts = cursor.fetchall()

    # ^^^^^SERVES SAME PURPOSES AS CODE BELOW

    # ***Using SQLAlechemy high-level SQL toolkit and Object-Relational Mapping (ORM) library all in python***
    # posts = (
    #     db.query(models.Post)
    #     .filter(models.Post.title.contains(search))
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )

    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Inserts the newly created title, content and publised info into the posts table in the database and returns the query
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # stores the returned query in new_post variable
    # new_post = cursor.fetchone()

    # # Updates change to database
    # conn.commit()

    # ^^^^^SERVES SAME PURPOSES AS CODE BELOW
    # Creates brand new post with given attributes
    # print(current_user.id)
    # print(current_user.email)
    new_post = models.Post(
        owner_id=current_user.id,
        # Instead of having to type out each one of the fields like this
        # title=post.title, content=post.content, published=post.published
        # We can just upack the dictionary that pydantic turned our model into like so
        **post.model_dump(),
    )
    # Adds new post to database
    db.add(new_post)
    # Commits changes to database
    db.commit()
    # Retrieve post that was created and store it back into new_post variable
    db.refresh(new_post)

    return new_post


# {id} is a path parameter
# it will send the id of the posts
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # # Gets the the post with matching id from database
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
    # # stores the retrieved post in the post variable
    # post = cursor.fetchone()
    # Queries into model we are intreseted in getting the filtered id and selecting the posts that match that id using .first()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    # Checks if the post exisits
    if not post:
        # raise Exception instead of return error code (cleaner)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    # Returns the post
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # # Deletes the posts from the database with matching id's
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (id,))
    # # Gets the deleted post
    # deleted_post = cursor.fetchone()
    # # Make changes to database
    # conn.commit()

    # queries for the post table in models then filters out the passed id
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # checks if the posts is equal to None
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    # Deletes the post, instructing SQLAlchemy not to synchronize the session after the delete operation
    post_query.delete(synchronize_session=False)

    # Commits the changes to the database
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
# grab the id and post from the frontend
def update_post(
    id: int,
    update_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # # Updates retrieved post title, content, and published attritubes
    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, (id,)),
    # )
    # # stores the updated posts in a variable
    # updated_post = cursor.fetchone()

    # # commits changes to database
    # conn.commit()

    # Set up query to find post with specific id
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # Grab that specific post
    post = post_query.first()

    # check if the post exsist in the database
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    # If it does exsist, updates the post_query by obtaining a dictionary representation of the post object
    post_query.update(update_post.model_dump(), synchronize_session=False)

    # Persist the changes permanently
    db.commit()

    # return
    return post_query.first()
