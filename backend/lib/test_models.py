import pytest
from pydantic import ValidationError

from lib.models import (
    FeedbackRating,
    Listing,
    ScoredListing,
    SearchStrategy,
    StyleFeature,
    StyleProfile,
    UserPreferences,
)


def make_listing(**overrides):
    return {
        "id": "123",
        "title": "Vintage jacket",
        "price": 25.0,
        "vinted_url": "https://vinted.com/items/123",
        **overrides,
    }


def test_style_feature_valid():
    f = StyleFeature(label="muted earth tones", confidence=0.8, examples=["url1"])
    assert f.confidence == 0.8


def test_style_feature_rejects_confidence_above_1():
    with pytest.raises(ValidationError):
        StyleFeature(label="x", confidence=1.1, examples=[])


def test_style_feature_rejects_confidence_below_0():
    with pytest.raises(ValidationError):
        StyleFeature(label="x", confidence=-0.1, examples=[])


def test_style_profile_valid():
    p = StyleProfile(board_ids=["board-1"])
    assert p.features == []
    assert p.id is None
    assert p.created_at is None


def test_user_preferences_defaults():
    prefs = UserPreferences()
    assert prefs.sizes == []
    assert prefs.price_min is None


def test_user_preferences_rejects_negative_price():
    with pytest.raises(ValidationError):
        UserPreferences(price_min=-1.0)


def test_search_strategy_inherits_prefs():
    s = SearchStrategy(keywords=["linen trousers"], sizes=["M"], price_max=50.0)
    assert s.sizes == ["M"]
    assert s.price_max == 50.0
    assert s.keywords == ["linen trousers"]


def test_listing_valid():
    listing = Listing(**make_listing())
    assert listing.feedback is None


def test_listing_rejects_negative_price():
    with pytest.raises(ValidationError):
        Listing(**make_listing(price=-5.0))


def test_listing_feedback_valid_ratings():
    for rating in (1, 2, 3, 4, 5):
        listing = Listing(**make_listing(feedback=rating))
        assert listing.feedback == FeedbackRating(rating)


def test_listing_feedback_rejects_out_of_range():
    with pytest.raises(ValidationError):
        Listing(**make_listing(feedback=6))


def test_scored_listing_requires_score_and_reasoning():
    scored = ScoredListing(**make_listing(score=8.5, reasoning="Great silhouette match"))
    assert scored.score == 8.5
    assert scored.reasoning == "Great silhouette match"


def test_scored_listing_missing_score_fails():
    with pytest.raises(ValidationError):
        ScoredListing(**make_listing(reasoning="some reason"))


def test_scored_listing_is_listing():
    scored = ScoredListing(**make_listing(score=7.0, reasoning="Nice"))
    assert isinstance(scored, Listing)
