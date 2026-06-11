from utils.analysis import calculate_wpm, count_fillers, top_words, total_words


def test_total_words_counts_transcript_tokens() -> None:
    assert total_words("Hello, brave new speaker!") == 4


def test_count_fillers_matches_common_phrases() -> None:
    assert count_fillers("Um, you know, this is actually useful.") == 3


def test_calculate_wpm_guards_zero_duration() -> None:
    assert calculate_wpm("one two three", 0) == 0.0


def test_top_words_filters_stop_words() -> None:
    assert top_words("the voice voice clarity and pace", limit=2) == {"voice": 2, "clarity": 1}
