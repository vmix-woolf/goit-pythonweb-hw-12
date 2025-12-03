from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=False, nullable=False)
    phone = Column(String(50), nullable=False)
    birthday = Column(Date, nullable=True)
    additional_info = Column(String(255), nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Зв’язок з користувачем
    owner = relationship("User", back_populates="contacts")
