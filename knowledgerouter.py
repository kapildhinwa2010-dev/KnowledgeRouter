# KnowledgeRouter - Route queries to the expert that knows the most about them
# Part of the Kapildhinwa2010-dev Toolkit.

"""KnowledgeRouter - coverage-based query routing.

Lineage: DNA_DYNIMO routers. Each expert declares the topics it knows.
A query is a set of topic tokens; the router sends it to the expert with
the highest topic coverage, breaking ties by lower cost.

This is lexical topic matching, not semantic understanding: a query about
an unlisted synonym scores zero coverage. See README limitations.
"""

from __future__ import annotations

__all__ = ["knowledge_coverage", "TopicExpert", "KnowledgeRouter"]


def knowledge_coverage(query_topics, expert_topics) -> float:
    """Fraction of query topics the expert knows. 1.0 means full coverage."""
    query = set(query_topics)
    if not query:
        raise ValueError("query_topics must be non-empty")
    known = query & set(expert_topics)
    return len(known) / len(query)


class TopicExpert:
    """A routing target that answers queries about its declared topics."""

    def __init__(self, name: str, topics, cost: float = 1.0) -> None:
        if not name:
            raise ValueError("name must be non-empty")
        topics = set(topics)
        if not topics:
            raise ValueError("topics must be non-empty")
        if cost < 0:
            raise ValueError("cost must be >= 0")
        self.name = name
        self.topics = topics
        self.cost = float(cost)
        self.calls = 0

    def handle(self, query_topics) -> str:
        coverage = knowledge_coverage(query_topics, self.topics)
        if coverage <= 0.0:
            raise ValueError("expert knows none of the query topics")
        self.calls += 1
        return "answered by {} (coverage {:.2f})".format(self.name, coverage)


class KnowledgeRouter:
    """Route each query to the highest-coverage expert, ties by lower cost."""

    def __init__(self) -> None:
        self.experts: list = []

    def add_expert(self, name: str, topics, cost: float = 1.0) -> None:
        self.experts.append(TopicExpert(name, topics, cost))

    def route(self, query_topics) -> TopicExpert:
        if not self.experts:
            raise ValueError("no experts registered")
        scored = []
        for expert in self.experts:
            cov = knowledge_coverage(query_topics, expert.topics)
            if cov > 0.0:
                scored.append((cov, expert))
        if not scored:
            raise ValueError("no expert knows any query topic")
        best = max(scored, key=lambda pair: (pair[0], -pair[1].cost))
        return best[1]

    def route_and_handle(self, query_topics) -> str:
        return self.route(query_topics).handle(query_topics)

    def usage_report(self) -> dict:
        return {e.name: e.calls for e in self.experts}
