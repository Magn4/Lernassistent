# Combines everything into the FastAPI application.
# Test comment
from fastapi import FastAPI, HTTPException
from schemas import UpdateCardRequest, UpdateCardResponse
from models import get_card, update_card_db
from services import update_card

app = FastAPI()

@app.post("/update-card", response_model=UpdateCardResponse)
async def update_card_endpoint(request: UpdateCardRequest):
    card = await get_card(request.card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    # Update card using the spaced repetition logic
    result = update_card(
        button=request.button,
        interval=card.interval,
        ef=card.ef,
        repetitions=card.repetitions,
        lapses=card.lapses,
    )

    # Save updated card to database
    await update_card_db(request.card_id, result)

    # Return response
    return UpdateCardResponse(
        card_id=request.card_id,
        next_interval=result["next_interval"],
        ef=result["new_ef"],
        repetitions=result["repetitions"],
        lapses=result["lapses"],
    )
