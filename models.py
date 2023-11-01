from connection import Base
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, Enum, text


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, unique=False, index=True)
    is_active = Column(Boolean, default=False)

    payment_forms = relationship("PaymentForm", back_populates="owner")


class PaymentForm(Base):
    __tablename__ = "payment_forms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    amount = Column(Float)
    currency = Column(String)
    unique_link = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum('Pending', 'Success', 'Failed'), default='Pending', nullable=False)

    owner = relationship("UserModel", back_populates="payment_forms")


class PaymentFormCreate(BaseModel):
    name: str
    description: str
    amount: float
    currency: str
