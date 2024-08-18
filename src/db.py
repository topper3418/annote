
import sqlite3
from typing import List
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship
from sqlalchemy import Column, ForeignKey, Table, create_engine


class Base(DeclarativeBase):
    pass


note_tag_table = Table(
    'note_tag_association', 
    Base.metadata,
    Column('note_id', ForeignKey('notes.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)


class NoteAssociation(Base):
    __tablename__ = 'note_associations'
    first_id: Mapped[int] = mapped_column(ForeignKey('notes.id'), primary_key=True)
    second_id: Mapped[int] = mapped_column(ForeignKey('notes.id'), primary_key=True)
    strength: Mapped[int]

    # Relations
    first_note: Mapped["Note"] = relationship("Note", foreign_keys=[first_id], back_populates="associations_from")
    second_note: Mapped["Note"] = relationship("Note", foreign_keys=[second_id], back_populates="associations_to")


class Note(Base):
    __tablename__ = 'notes'
    # data
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
    content: Mapped[str]
    completion: Mapped[bool | None] = mapped_column(default=False)
    # foreign keys
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('notes.id'))
    # relations
    parent: Mapped["Note"] = relationship("Note", remote_side=[id], back_populates="children")
    children: Mapped[List["Note"]] = relationship("Note", back_populates="parent")
    task: Mapped["Task"] = relationship("Task", uselist=False, back_populates="note")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=note_tag_table, back_populates="notes")
    # Note associations
    associations_from: Mapped[List["NoteAssociation"]] = relationship("NoteAssociation", foreign_keys=[NoteAssociation.first_id], back_populates="first_note")
    associations_to: Mapped[List["NoteAssociation"]] = relationship("NoteAssociation", foreign_keys=[NoteAssociation.second_id], back_populates="second_note")



class Task(Base):
    __tablename__ = 'tasks'
    # data
    id: Mapped[int] = mapped_column(primary_key=True)
    start_date: Mapped[datetime | None]
    due_date: Mapped[datetime | None]
    status: Mapped[str | None]
    active: Mapped[bool | None] = mapped_column(default=True)
    # foreign keys
    note_id: Mapped[int | None] = mapped_column(ForeignKey('notes.id'))
    # relations
    note: Mapped[Note] = relationship("Note", back_populates="task")


class Tag(Base):
    __tablename__ = 'tags'
    # data
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    # relations
    notes: Mapped[List[Note]] = relationship("Note", secondary=note_tag_table, back_populates="tags")


class Keyword(Base):
    __tablename__ = 'keywords'
    # data
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str]
    # relations
    source: Mapped[Note] = relationship("Note", back_populates="keywords")


engine = create_engine('sqlite:///notes.db', echo=True)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def create_note(content: str, is_completion: bool=False) -> Note:
    note = Note(content=content, completion=is_completion)
    with Session() as session:
        session.add(note)
        session.commit()
    return note


def create_tag(name: str, description: str) -> Tag:
    """Create a tag with the given name, if it doesn't already exist"""
    # check if it already exists
    with Session() as session:
        tag = session.query(Tag).filter_by(name=name).first()
        if tag:
            return tag
        tag = Tag(name=name, description=description)
        session.add(tag)
        session.commit()
    return tag