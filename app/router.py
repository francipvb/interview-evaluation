from typing import List
from fastapi import APIRouter, Response, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .schemas import TodoItem, TodoPayload, User, UserPayload
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
        credentials: HTTPBasicCredentials = Depends(security), 
        db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if user is None or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.get("/items/", response_model=List[TodoItem])
def get_items(db: Session = Depends(get_db)):
    """Retrieve a persistent list of items."""
    items = db.query(models.TodoItem).all()
    return items

@router.get("/items/{id}", response_model=TodoItem)
def get_item(id: int, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):
    """Retrieve a particular item from the store."""
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post(
    path="/items/",
    response_model=TodoItem,
    status_code=201,
    response_description="The item has been created successfully.",
)

def create_item(payload: TodoPayload, 
                user: User = Depends(get_current_user), 
                db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    item = models.TodoItem(**payload.model_dump(), username=user.username)
    db.add(item)
    db.commit()
    db.refresh(item)
    pydantic_item = TodoItem(**item.__dict__)

    return pydantic_item

@router.put("/items/{id}", response_model=TodoItem)
def update_item(id: int, 
                payload: TodoPayload, 
                user: User = Depends(get_current_user), 
                db: Session = Depends(get_db)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.username != user.username:
        raise HTTPException(status_code=403, detail="Permission denied")
    item.update_from_payload(payload)
    db.commit()
    db.refresh(item)
    pydantic_item = TodoItem(**item.__dict__)

    return pydantic_item

@router.delete("/items/{id}", 
               response_class=Response, 
               status_code=204)
def remove_item(id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.query(models.TodoItem).filter(models.TodoItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.username != user.username:
        raise HTTPException(status_code=403, detail="Permission denied")
    db.delete(item)
    db.commit()

@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserPayload, db: Session = Depends(get_db)):
    hashed_password = hash_password(payload.password) 
    user = models.User(
        username=payload.username, 
        password=hashed_password, 
        name=payload.name,
        email=payload.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users/me", response_model=User)
def get_current_user_endpoint(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user:
        return current_user
    raise HTTPException(status_code=401, detail="Authentication required")