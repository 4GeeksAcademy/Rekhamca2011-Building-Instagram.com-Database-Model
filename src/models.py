from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import enum
from datetime import datetime, timezone

db = SQLAlchemy()

class MediaType(enum.Enum):
    IMAGE = "image"
    OTHER = "other"

class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), primary_key=True)


class User(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class Media(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.ID"), nullable=False)


class Post(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), nullable=False)
    is_public: Mapped[bool] = mapped_column(default=True, nullable=False)


class Comment(db.Model):
    ID: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.ID"), nullable=False)

class Like(db.Model):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.ID"), primary_key=True)
    created_at: Mapped[str] = mapped_column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

class Share(db.Model):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.ID"), primary_key=True)
    created_at: Mapped[datetime] = db.mapped_column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)