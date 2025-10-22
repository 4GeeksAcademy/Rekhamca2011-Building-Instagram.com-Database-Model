from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from datetime import datetime, timezone

db = SQLAlchemy()


class MediaType(enum.Enum):
    IMAGE = "image"
    OTHER = "other"


class Follower(db.Model):
    
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), primary_key=True)

    follower: Mapped["User"] = relationship(
        "User", foreign_keys=[user_from_id], back_populates="following"
    )
    followed: Mapped["User"] = relationship(
        "User", foreign_keys=[user_to_id], back_populates="followers"
    )


class User(db.Model):

    ID: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    shares: Mapped[list["Share"]] = relationship("Share", back_populates="user", cascade="all, delete-orphan")

    followers: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys=[Follower.user_to_id],
        back_populates="followed",
        cascade="all, delete-orphan"
    )
    following: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys=[Follower.user_from_id],
        back_populates="follower",
        cascade="all, delete-orphan"
    )


class Post(db.Model):

    ID: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), nullable=False)
    is_public: Mapped[bool] = mapped_column(default=True, nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    shares: Mapped[list["Share"]] = relationship("Share", back_populates="post", cascade="all, delete-orphan")


class Media(db.Model):

    ID: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.ID"), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="media")


class Comment(db.Model):

    ID: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.ID"), nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class Like(db.Model):

    user_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.ID"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes")


class Share(db.Model):

    user_id: Mapped[int] = mapped_column(ForeignKey("user.ID"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.ID"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="shares")
    post: Mapped["Post"] = relationship("Post", back_populates="shares")
