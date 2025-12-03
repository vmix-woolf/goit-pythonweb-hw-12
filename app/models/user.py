from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)
    # Зв'язок з контактами
    contacts = relationship("Contact", back_populates="owner")
