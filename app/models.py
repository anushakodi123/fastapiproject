from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Column, DateTime, text, Boolean, String, ForeignKey

class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(
    default=True,
    sa_column=Column(Boolean, server_default=text("TRUE"), index=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
    user_id: int = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False
        )
    )

    user: Optional["User"] = Relationship(back_populates="posts")

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String, nullable=False, unique=True))
    password: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    )
    posts: List["Post"] = Relationship(back_populates="user")

class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    post_id: int = Field(
        sa_column=Column(
            ForeignKey("posts.id", ondelete="CASCADE"),
            nullable=False, primary_key=True
        )
    )
    user_id: int = Field(
        sa_column=Column(
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False, primary_key=True
        )
    )
