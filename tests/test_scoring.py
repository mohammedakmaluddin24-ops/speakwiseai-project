from utils.scoring import confidence_score, generate_feedback


def test_confidence_score_rewards_balanced_delivery() -> None:
    assert confidence_score(135, 0) == 100


def test_confidence_score_penalizes_fast_speech_and_fillers() -> None:
    assert confidence_score(190, 4) == 73


def test_generate_feedback_for_balanced_delivery() -> None:
    assert generate_feedback(135, 0) == ["Excellent delivery: your pace is balanced and filler usage is low."]
