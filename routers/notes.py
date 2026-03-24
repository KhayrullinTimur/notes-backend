from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models import Note, User
from schemas import NoteCreate, NoteUpdate, NoteResponse
from database import get_db
from security import get_current_user

router = APIRouter()


@router.post("/notes", response_model=NoteResponse)
def note_add(
    note: NoteCreate,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    
    db_note = Note(
        text=note.text,
        user_id=current_user.id
    )
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/notes", response_model=list[NoteResponse])
def get_notes(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    query = db.query(Note).filter(Note.user_id == current_user.id)

    if search:
        query = query.filter(Note.text.ilike(f"%{search}%"))

    notes = query.limit(limit).offset(offset).all()
    
    return notes

@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    note = db.query(Note).filter(Note.id == note_id).first()
    
    if note is None:
        raise HTTPException(status_code=404, detail="Note not Found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return note

@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int, update_note: NoteUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):

    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not Found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    note.text = update_note.text
    db.commit()
    db.refresh(note)
    
    return note

@router.delete("/notes/{note_id}")
def del_note(
    note_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    note = db.query(Note).filter(Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not Found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(note)
    db.commit()

    return {"message": "Note deleted"}
