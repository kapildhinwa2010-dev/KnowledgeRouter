"""Tests for KnowledgeRouter: topic-coverage routing."""

import pytest

from knowledgerouter import KnowledgeRouter, TopicExpert, knowledge_coverage


def test_coverage_full_partial_zero():
    assert knowledge_coverage(["a", "b"], ["a", "b", "c"]) == 1.0
    assert knowledge_coverage(["a", "b"], ["a", "x"]) == 0.5
    assert knowledge_coverage(["a"], ["x", "y"]) == 0.0


def test_coverage_empty_query_raises():
    with pytest.raises(ValueError):
        knowledge_coverage([], ["a"])


def test_expert_validation():
    with pytest.raises(ValueError):
        TopicExpert("", ["a"])
    with pytest.raises(ValueError):
        TopicExpert("e", [])
    with pytest.raises(ValueError):
        TopicExpert("e", ["a"], cost=-1.0)


def test_route_picks_highest_coverage():
    router = KnowledgeRouter()
    router.add_expert("general", ["math", "physics"], cost=1.0)
    router.add_expert("specialist", ["math"], cost=5.0)
    expert = router.route(["math", "physics"])
    assert expert.name == "general"


def test_route_tie_breaks_by_lower_cost():
    router = KnowledgeRouter()
    router.add_expert("cheap", ["math"], cost=1.0)
    router.add_expert("pricey", ["math"], cost=9.0)
    assert router.route(["math"]).name == "cheap"


def test_route_no_expert_knows_topic_raises():
    router = KnowledgeRouter()
    router.add_expert("e", ["math"])
    with pytest.raises(ValueError):
        router.route(["biology"])


def test_route_empty_router_raises():
    with pytest.raises(ValueError):
        KnowledgeRouter().route(["math"])


def test_route_and_handle_and_report():
    router = KnowledgeRouter()
    router.add_expert("e", ["math"])
    out = router.route_and_handle(["math"])
    assert "answered by e" in out
    assert router.usage_report() == {"e": 1}
