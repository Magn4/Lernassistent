import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Card, Deck
from datetime import datetime, timedelta

DATABASE_URL = f"postgresql://{os.getenv('DB_USER', 'db_user')}:{os.getenv('DB_PASSWORD', 'password123')}@{os.getenv('DB_HOST', 'database')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'app_db')}"

class AnkiDatabaseContext:
    def __init__(self, db_url=DATABASE_URL):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def create_card(self, front, back, deck_id):
        session = self.Session()
        try:
            new_card = Card(front=front, back=back, deck_id=deck_id)
            session.add(new_card)
            session.commit()
            session.refresh(new_card)
            return new_card
        except Exception as e:
            session.rollback()
            print(f"Error creating card: {e}")
        finally:
            session.close()

    def get_card(self, card_id):
        session = self.Session()
        try:
            return session.query(Card).get(card_id)
        except Exception as e:
            print(f"Error fetching card: {e}")
        finally:
            session.close()

    def update_card_db(self, card_id, result):
        session = self.Session()
        try:
            card = session.query(Card).get(card_id)
            if not card:
                raise ValueError(f"Card with ID {card_id} does not exist.")
            
            card.interval = result["next_interval"]
            card.ef = result["new_ef"]
            card.repetitions = result["repetitions"]
            card.lapses = result["lapses"]
            card.next_review = datetime.utcnow() + timedelta(days=card.interval)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating card: {e}")
        finally:
            session.close()

    def create_deck(self, name, description=None):
        session = self.Session()
        try:
            new_deck = Deck(name=name, description=description)
            session.add(new_deck)
            session.commit()
            session.refresh(new_deck)
            return new_deck
        except Exception as e:
            session.rollback()
            print(f"Error creating deck: {e}")
        finally:
            session.close()

    def update_deck(self, deck_id, name=None, description=None):
        session = self.Session()
        try:
            deck = session.query(Deck).get(deck_id)
            if not deck:
                return None

            if name:
                deck.name = name
            if description:
                deck.description = description

            session.commit()
            session.refresh(deck)
            return deck
        except Exception as e:
            session.rollback()
            print(f"Error updating deck: {e}")
        finally:
            session.close()

    def get_next_review_card(self):
        session = self.Session()
        try:
            return session.query(Card).filter(Card.next_review <= datetime.utcnow()).first()
        except Exception as e:
            print(f"Error fetching next review card: {e}")
        finally:
            session.close()

    def get_deck(self, deck_id):
        session = self.Session()
        try:
            return session.query(Deck).get(deck_id)
        except Exception as e:
            print(f"Error fetching deck: {e}")
        finally:
            session.close()

    def get_all_decks(self):
        session = self.Session()
        try:
            return session.query(Deck).all()
        except Exception as e:
            print(f"Error fetching decks: {e}")
        finally:
            session.close()

    def get_cards_in_deck(self, deck_id):
        session = self.Session()
        try:
            return session.query(Card).filter(Card.deck_id == deck_id).all()
        except Exception as e:
            print(f"Error fetching cards in deck: {e}")
        finally:
            session.close()

    def delete_card(self, card_id):
        session = self.Session()
        try:
            card = session.query(Card).get(card_id)
            if not card:
                return None

            session.delete(card)
            session.commit()
            return card
        except Exception as e:
            session.rollback()
            print(f"Error deleting card: {e}")
        finally:
            session.close()

    def delete_deck(self, deck_id):
        session = self.Session()
        try:
            deck = session.query(Deck).get(deck_id)
            if not deck:
                return None

            session.delete(deck)
            session.commit()
            return deck
        except Exception as e:
            session.rollback()
            print(f"Error deleting deck: {e}")
        finally:
            session.close()

    def delete_all_decks(self):
        session = self.Session()
        try:
            session.query(Deck).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error deleting all decks: {e}")
        finally:
            session.close()
