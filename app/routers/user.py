from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

#
router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # has the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Convert the user schema object to a dictionary and unpack it to create a new User model instance
    new_user = models.User(**user.model_dump())
    # Add the new_user object to the database session
    db.add(new_user)
    # Commit the changes to the database to persist the new user
    db.commit()
    # Refresh the new_user object to ensure it reflects the current state in the database
    db.refresh(new_user)

    # Return the newly created user as the API response
    return new_user


# Gets the a users information
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    # Quiers database and gets the users info that matches id
    user = db.query(models.User).filter(models.User.id == id).first()

    # Validates that a correct user was sent
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user
