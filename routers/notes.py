from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models import User
from schemas import NoteCreate, NoteUpdate, NoteResponse
from database import get_db
from security import get_current_user
from services.note_service import create_note, get_notes, get_note_by_id, update_note, delete_note

router = APIRouter()


@router.post("/notes", response_model=NoteResponse)
def note_add(
    note: NoteCreate,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return create_note(db, note, current_user)

@router.get("/notes", response_model=list[NoteResponse])
def get_notes_endpoint(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return get_notes(db, current_user, limit, offset, search)

@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    return get_note_by_id(db, note_id, current_user)

@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note_endpoint(
    note_id: int, update_data: NoteUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    return update_note(db, note_id, update_data, current_user)

@router.delete("/notes/{note_id}")
def del_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    return delete_note(db, note_id, current_user)

