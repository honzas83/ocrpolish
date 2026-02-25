from ocrpolish.utils.nlp import get_word_set, overlap_coefficient


def test_get_word_set() -> None:
    text = "Hello, World! This is a test."
    words = get_word_set(text)
    # Preservation of case
    assert words == frozenset({"Hello", "World", "This", "is", "a", "test"})


def test_overlap_coefficient_exact() -> None:
    s1 = get_word_set("The quick brown fox")
    s2 = get_word_set("The quick brown fox")
    assert overlap_coefficient(s1, s2) == 1.0


def test_overlap_coefficient_partial() -> None:
    s1 = get_word_set("The quick brown fox")
    s2 = get_word_set("The quick white fox")
    # 3 out of 4 words match: "The", "quick", "fox"
    assert overlap_coefficient(s1, s2) == 0.75


def test_overlap_coefficient_empty() -> None:
    assert overlap_coefficient(frozenset(), frozenset()) == 0.0
