from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, NoteResponse, Token
from security import hash_password, verify_password, create_access_token


router = APIRouter()

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session=Depends(get_db)):

    hashed_password = hash_password(user.password)

    db_user = User(
        name=user.name,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=list[UserResponse])
def get_users(db: Session=Depends(get_db)):
    users = db.query(User).all()
    return users

@router.get("/users/{user_id}/notes", response_model=list[NoteResponse])
def get_user_note(user_id: int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.notes

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):   
    user = db.query(User).filter(User.name == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.name})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    } 
