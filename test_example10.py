def test_phrase_is_less_than_15_symbols():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"Phrase '{phrase}' is longer than 15 symbols"