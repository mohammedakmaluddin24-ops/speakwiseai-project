def confidence_score(wpm: float, fillers: int) -> int:
    """Score delivery quality out of 100 using pace and filler penalties."""
    score = 100

    if wpm < 110:
        score -= min(30, int((110 - wpm) * 0.5))
    elif wpm > 160:
        score -= min(30, int((wpm - 160) * 0.5))

    if fillers > 0:
        score -= min(35, fillers * 3)

    return max(0, min(100, int(score)))


def generate_feedback(wpm: float, fillers: int) -> list[str]:
    """Generate practical public-speaking feedback from pace and filler data."""
    feedback = []

    if fillers > 8:
        feedback.append("Reduce filler words by pausing briefly before your next point.")
    elif fillers > 0:
        feedback.append("Good control overall; trim a few filler words for a cleaner delivery.")

    if wpm > 160:
        feedback.append("Speak slower so listeners have time to absorb your ideas.")
    elif 0 < wpm < 110:
        feedback.append("Speak faster to keep energy and momentum in your delivery.")

    if not feedback:
        feedback.append("Excellent delivery: your pace is balanced and filler usage is low.")

    return feedback
