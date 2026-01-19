"""Tests for query expansion service."""

import pytest
from app.services.query_expansion import expand_query


def test_expand_single_abbreviation():
    """Test expanding a single abbreviation."""
    result = expand_query("ML research")
    assert "machine learning" in result
    assert "ML research" in result


def test_expand_multiple_abbreviations():
    """Test expanding multiple abbreviations in one query."""
    result = expand_query("ML and NLP")
    assert "machine learning" in result
    assert "natural language processing" in result
    assert "ML and NLP" in result


def test_no_expansion_needed():
    """Test that queries without abbreviations remain unchanged."""
    query = "machine learning algorithms"
    result = expand_query(query)
    assert result == query


def test_case_insensitive_expansion():
    """Test that abbreviations work regardless of case."""
    result_upper = expand_query("ML research")
    result_lower = expand_query("ml research")
    result_mixed = expand_query("Ml research")

    assert "machine learning" in result_upper
    assert "machine learning" in result_lower
    assert "machine learning" in result_mixed


def test_punctuation_handling():
    """Test that punctuation doesn't prevent expansion."""
    result = expand_query("ML, AI, and DL.")
    assert "machine learning" in result
    assert "artificial intelligence" in result
    assert "deep learning" in result


def test_partial_word_no_expansion():
    """Test that abbreviations as part of words don't get expanded."""
    query = "ملت research"  # Contains ML as part of a word
    result = expand_query(query)
    # Should not expand since ML is not a standalone word
    assert query in result


def test_biology_abbreviations():
    """Test expansion of biology-related abbreviations."""
    result = expand_query("DNA and RNA sequencing")
    assert "deoxyribonucleic acid" in result
    assert "ribonucleic acid" in result


def test_systems_abbreviations():
    """Test expansion of systems-related abbreviations."""
    result = expand_query("HPC and IoT")
    assert "high performance computing" in result
    assert "internet of things" in result


def test_multiple_same_abbreviation():
    """Test that the same abbreviation multiple times only adds expansion once."""
    result = expand_query("ML for ML applications")
    # Should only add "machine learning" once at the end
    count = result.count("machine learning")
    assert count == 1
