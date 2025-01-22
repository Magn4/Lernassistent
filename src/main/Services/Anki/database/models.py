from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    front = Column(String, nullable=False)
    back = Column(String, nullable=False)
    next_review = Column(DateTime, nullable=True, default=None)
    deck_id = Column(Integer, ForeignKey("decks.id"), nullable=False)
    interval = Column(Integer, default=1, nullable=False)
    ef = Column(Float, default=2.5, nullable=False)
    repetitions = Column(Integer, default=0, nullable=False)
    lapses = Column(Integer, default=0, nullable=False)
    
    deck = relationship('Deck', back_populates='cards')

class Deck(Base):
    __tablename__ = 'decks'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    cards = relationship('Card', back_populates='deck')
