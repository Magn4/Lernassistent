# The core spaced repetition algorithm resides here.


def update_card(button, interval, ef, repetitions, lapses):
    if button == "Again":
        interval = 10 / 60  # 10 minutes in fractional days
        repetitions = 0
        lapses += 1
    elif button == "Hard":
        interval = max(1, interval * 1.2)
        ef = max(1.3, ef - 0.15)
    elif button == "Good":
        interval = interval * ef
        repetitions += 1
    elif button == "Easy":
        interval = interval * ef * 1.3
        ef = min(3.0, ef + 0.15)
        repetitions += 1

    return {
        "next_interval": interval,
        "new_ef": ef,
        "repetitions": repetitions,
        "lapses": lapses,
    }
