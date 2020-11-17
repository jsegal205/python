import pytest

from is_palindrome import is_palindrome


def test_no_input_returns_true():
    assert is_palindrome("") == True


def test_single_letter_returns_true():
    assert is_palindrome("a") == True


def test_multiple_letters_returns_true():
    assert is_palindrome("abcba") == True


def test_non_palindrome_returns_false():
    assert is_palindrome("abc") == False


def test_with_centered_space_returns_true():
    assert is_palindrome("abc cba") == True


def test_with_off_centered_space_returns_true():
    assert is_palindrome("taco cat") == True


def test_mixed_casing_returns_true():
    assert is_palindrome("AbCcba") == True


def test_empty_list_returns_true():
    assert is_palindrome([]) == True


def test_single_element_list_returns_true():
    assert is_palindrome(["a"]) == True


def test_multiple_element_list_returns_true():
    assert is_palindrome(["a", "b", "c", "b", "a"]) == True


def test_mixed_case_multiple_element_list_returns_true():
    assert is_palindrome(["A", "B", "c", "b", "a"]) == True


def test_non_palindrome_multiple_element_list_returns_false():
    assert is_palindrome(["a", "b", "c"]) == False


def test_numbers_returns_true():
    assert is_palindrome(123321) == True


def test_non_palindrome_numbers_returns_false():
    assert is_palindrome(12345) == False
