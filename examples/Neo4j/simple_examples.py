
import logging
import os
from json import dumps
from textwrap import dedent
from typing import cast

import neo4j

from neo4j import GraphDatabase, basic_auth
from typing_extensions import LiteralString

driver = GraphDatabase.driver("bolt://localhost:7687",
                              auth=basic_auth("dbuser", "dbuserdbuser"))

#
# Copied from GitHub example.
def query(q: LiteralString) -> LiteralString:
    # this is a safe transform:
    # no way for cypher injection by trimming whitespace
    # hence, we can safely cast to LiteralString
    return cast(LiteralString, dedent(q).strip())


def t1():
    records, _, _ = driver.execute_query(
        query("""
            MATCH (m:Movie)<-[:ACTED_IN]-(a:Person)
            RETURN m.title AS movie, collect(a.name) AS cast
            LIMIT $limit
        """),
        limit=10
    )

    print("Records = ", records)


if __name__ == "__main__":
    t1()