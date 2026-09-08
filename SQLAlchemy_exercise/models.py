from typing import List, Optional

from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Relationship, relationship

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    # chef_id = Column(Integer, ForeignKey('chefs.id'))
    # chef = Relationship('Chef', back_populates='recipes')
    chef_id: Mapped[Optional[int]] = mapped_column(ForeignKey('chefs.id'))
    chef: Mapped[Optional['Chef']] = relationship(back_populates='recipes')


class Chef(Base):
    __tablename__ = "chefs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    recipes: Mapped[List['Recipe']] = relationship(back_populates='chef')
