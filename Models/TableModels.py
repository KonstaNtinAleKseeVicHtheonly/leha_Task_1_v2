from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Float, DateTime, func, Integer
from dataclasses import dataclass


@dataclass
class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


@dataclass
class Attributes(Base):
    __tablename__ = 'Employees'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    vacant: Mapped[str] = mapped_column(String(20), nullable=False)
    salary: Mapped[float] = mapped_column(Float, asdecimal=True,  nullable=True) # correct
    description: Mapped[str] = mapped_column(String())
    id_user_tg: Mapped[int] = mapped_column(Integer, nullable=False)
    
    
