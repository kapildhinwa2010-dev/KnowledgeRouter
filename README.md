# KnowledgeRouter

[![CI](https://github.com/kapildhinwa2010-dev/KnowledgeRouter/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/KnowledgeRouter/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kapildhinwa2010-dev/KnowledgeRouter/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/KnowledgeRouter/actions/workflows/codeql.yml)

Route queries to the expert that knows the most about them, by lexical topic coverage.

## What it does

Each expert declares the set of topics it can answer. A query is a set of topic
tokens. The router computes the fraction of query topics each expert covers and
sends the query to the highest-coverage expert, breaking ties by lower cost.

    from knowledgerouter import KnowledgeRouter

    router = KnowledgeRouter()
    router.add_expert("general", ["math", "physics"], cost=1.0)
    router.add_expert("algebra", ["math", "algebra"], cost=2.0)
    print(router.route_and_handle(["math", "algebra"]))

## API

- knowledge_coverage(query_topics, expert_topics) - fraction of query topics known
- TopicExpert(name, topics, cost) - one routing target
- KnowledgeRouter.add_expert / route / route_and_handle / usage_report

## Honest results and limitations

- This is lexical set matching, not semantic understanding. A query about
  "linear algebra" scores zero against an expert that only lists "algebra".
- Coverage ignores how deep an expert knows a topic; one overlapping token
  counts the same as full expertise.
- No learning: coverage comes only from the topic sets you declare.

## Status

Part of the kapildhinwa2010-dev toolkit experiments. CI and CodeQL run on
every push to main. License: MIT.
