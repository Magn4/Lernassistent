from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String

DATABASE_URL = "sqlite:///./anki.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

cards = Table(
    "cards",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("ef", Float, default=2.5),  # Ease Factor
    Column("interval", Float, default=1.0),  # Review Interval in days
    Column("repetitions", Integer, default=0),  # Successful repetitions
    Column("lapses", Integer, default=0),  # Number of lapses
)

# Create the database
metadata.create_all(bind=engine)
