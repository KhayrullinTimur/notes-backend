from models import Note
from fastapi import HTTPException

def create_note(db, note, current_user):
    db_note = Note(
        text=note.text,
        user_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_notes(db, current_user, limit:int, offset:int, search: str | None):
    query = db.query(Note).filter(Note.user_id == current_user.id)
    if search:
        query = query.filter(Note.text.ilike(f"%{search}%"))
    return query.limit(limit).offset(offset).all()

def get_note_by_id(db, note_id, current_user):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

def update_note(db, note_id, update_data, current_user):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    note.text = update_data.text
    db.commit()
    db.refresh(note)
    return note

def delete_note(db, note_id, current_user):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
