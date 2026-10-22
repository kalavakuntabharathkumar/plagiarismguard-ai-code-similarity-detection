from app.similarity import compare_sources, normalize_python


def test_variable_renaming_is_normalized():
    left = normalize_python("total = price + tax")
    right = normalize_python("amount = cost + fee")
    assert left == right


def test_identical_program_has_high_similarity():
    result = compare_sources("print(2 + 2)", "print(2 + 2)")
    assert result["similarity_percent"] > 90
    assert result["review_recommended"] is True


def test_different_programs_return_bounded_score():
    result = compare_sources("print('hello')", "for i in range(10): print(i * 3)")
    assert 0 <= result["similarity_percent"] <= 100


def test_emptyish_normalization_does_not_crash():
    assert isinstance(normalize_python(""), str)
