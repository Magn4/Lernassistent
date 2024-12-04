# We use Pydantic to validate incoming data.

from pydantic import BaseModel

class UpdateCardRequest(BaseModel):
    card_id: int
    button: str  # One of ["Again", "Hard", "Good", "Easy"]

class UpdateCardResponse(BaseModel):
    card_id: int
    next_interval: float
    ef: float
    repetitions: int
    lapses: int
