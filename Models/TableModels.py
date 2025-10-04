from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Float, DateTime, func, Integer
from dataclasses import dataclass


@dataclass
class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


@dataclass
class Attributes(Base):
    __tablename__ = 'AYE'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    city: Mapped[str] = mapped_column(String(50))
    social_status: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(150))
    id_telegram_user: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    messages: Mapped[int] = mapped_column(Integer, nullable=False)
    strikes: Mapped[int] = mapped_column(Integer, nullable=False)
    
    def __str__(self):
            return (
                f"👤 Информация о пользователе:\n"
                f"Имя: {self.name}\n"
                f"Возраст: {self.age}\n" 
                f"Город: {self.city}\n"
                f"Статус: {self.social_status}\n"
                f"Описание: {self.description}"
            )