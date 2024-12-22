# Helper functions to interact with the database.


from sqlalchemy import select, update
from database import engine, cards

async def get_card(card_id):
    query = select(cards).where(cards.c.id == card_id)
    async with engine.connect() as conn:
        result = await conn.execute(query)
        return result.fetchone()

async def update_card_db(card_id, data):
    query = (
        update(cards)
        .where(cards.c.id == card_id)
        .values(
            interval=data["next_interval"],
            ef=data["new_ef"],
            repetitions=data["repetitions"],
            lapses=data["lapses"],
        )
    )
    async with engine.connect() as conn:
        await conn.execute(query)
        await conn.commit()
