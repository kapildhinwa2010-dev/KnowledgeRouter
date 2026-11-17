# KnowledgeRouter

KnowledgeRouter is a small Python module that routes a query represented as topic tokens to a registered expert based on exact topic overlap. It is a basic, experimental implementation of lexical routing, not a semantic search or expert-invocation service.

## How routing works

Each expert has a name, a non-empty set of topics, and a numeric cost. For each expert, the router calculates coverage as the fraction of the query's distinct topics that appear in the expert's topic set. It selects an expert with the highest coverage; if coverage is tied, it selects the lower-cost expert. Experts with zero overlap are not selected. If the query is empty, no experts are registered, or no expert overlaps the query, the corresponding operation raises `ValueError`.

`route()` returns the selected `TopicExpert`. `route_and_handle()` calls that expert's `handle()` method, which increments its call counter and returns a formatted text string; it does not invoke an external model, service, or user-supplied expert callback. `usage_report()` returns the call counts keyed by expert name.

## Installation

The project includes setuptools build metadata and can be installed from the repository root:

```bash
python -m pip install .
```

The package metadata requires Python 3.9 or newer and declares `numpy>=1.24` as a dependency.

## Example

```python
from knowledgerouter import KnowledgeRouter

router = KnowledgeRouter()
router.add_expert("general", ["math", "physics"], cost=1.0)
router.add_expert("algebra", ["math", "algebra"], cost=2.0)

expert = router.route(["math", "algebra"])
print(expert.name)  # algebra: full coverage, versus partial coverage for general
print(router.route_and_handle(["math"]))
print(router.usage_report())
```

The matching is set-based and exact: topic values must match as supplied. The module does not tokenize free-form text; callers must provide topic collections themselves.

## API

- `knowledge_coverage(query_topics, expert_topics)` returns the fraction of distinct query topics found in an expert's topic collection. An empty query raises `ValueError`.
- `TopicExpert(name, topics, cost=1.0)` represents a named routing target. The name and topic set must be non-empty, and cost must be non-negative.
- `KnowledgeRouter.add_expert(name, topics, cost=1.0)` registers an expert.
- `KnowledgeRouter.route(query_topics)` selects and returns an expert.
- `KnowledgeRouter.route_and_handle(query_topics)` routes and returns the selected expert's formatted response string.
- `KnowledgeRouter.usage_report()` reports counts of calls to `handle()` by expert name.

## Tests and CI

On commit `b37968d9e79e46b2e0a484aadc65dca252edd421`, the local test command `python -m pytest -q` completed with **8 passed**. The repository defines a GitHub Actions test workflow for Python 3.10, 3.11, and 3.12, including pytest, compilation, and an import smoke test. A CodeQL workflow is also configured. Their GitHub-hosted results were not verified for this commit.

No benchmark or measured performance results are provided.

## Scope and limitations

- Matching is exact lexical set overlap, not semantic understanding, synonym matching, or free-text interpretation.
- Coverage only measures the share of query topics present in a declared topic set; it does not evaluate expertise quality or answer accuracy.
- Cost only breaks ties between experts with equal coverage. It is not a general latency or resource optimizer.
- `TopicExpert.handle()` returns a placeholder formatted string rather than calling a real expert implementation.
- Topic sets are supplied by the caller; the project does not learn, update, persist, or discover expertise.
- The repository provides a compact module and unit tests, not a hosted service, command-line interface, or production deployment setup.

## Status

Project metadata identifies version `0.1.0`. The available implementation is a small, tested Python module; no broader release, production-readiness, or performance claim is made here.

## License

The repository includes an MIT License in `LICENSE`, with copyright notice `Copyright (c) 2026 Kapildhinwa2010-dev`. See that file for the complete terms.
