#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Copyright 2011-2018, Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Pygments lexer for Cypher.
"""

import re

from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Keyword, Punctuation, Comment, Operator, Name, \
    String, Number, Whitespace


__all__ = ["cypher_keywords", "CypherLexer"]


cypher_keywords = [
    "AS",
    "ASC",
    "ASCENDING",
    "ASSERT",
    "ASSERT EXISTS",
    "CALL",
    "CONSTRAINT ON",
    "CREATE",
    "CREATE UNIQUE",
    "CYPHER",
    "DELETE",
    "DESC",
    "DESCENDING",
    "DETACH DELETE",
    "DO",
    "DROP",
    "EXPLAIN",
    "FIELDTERMINATOR",
    "FOREACH",
    "FROM",
    "GRAPH",
    "GRAPH AT",
    "GRAPH OF",
    "INDEX ON",
    "INTO",
    "IS NODE KEY",
    "IS UNIQUE",
    "LIMIT",
    "LOAD",
    "LOAD CSV",
    "MATCH",
    "MERGE",
    "ON CREATE SET",
    "ON MATCH SET",
    "OPTIONAL MATCH",
    "ORDER BY",
    "PERSIST",
    "_PRAGMA",
    "PROFILE",
    "REMOVE",
    "RELOCATE",
    "RETURN",
    "RETURN DISTINCT",
    "SET",
    "SKIP",
    "SNAPSHOT",
    "SOURCE",
    "START",
    "TARGET",
    "UNION",
    "UNION ALL",
    "UNWIND",
    "USING INDEX",
    "USING JOIN ON",
    "USING PERIODIC COMMIT",
    "USING SCAN",
    "WHERE",
    "WITH",
    "WITH DISTINCT",
    "WITH HEADERS",
    "YIELD",
    ">>",
]
cypher_pseudo_keywords = [
    "BEGIN",
    "COMMIT",
    "ROLLBACK",
]
cypher_operator_symbols = [
    "!=",
    "%",
    "*",
    "+",
    "+=",
    "-",
    ".",
    "/",
    "<",
    "<=",
    "<>",
    "=",
    "=~",
    ">",
    ">=",
    "^",
]
cypher_operator_words = [
    'AND',
    'CASE',
    'CONTAINS',
    'DISTINCT',
    'ELSE',
    'END',
    'ENDS WITH',
    'IN',
    'IS NOT NULL',
    'IS NULL',
    'NOT',
    'OR',
    'STARTS WITH',
    'THEN',
    'WHEN',
    'XOR',
]
cypher_constants = [
    'null',
    'true',
    'false',
]

neo4j_built_in_functions = [
    "abs",
    "acos",
    "all",
    "allShortestPaths",
    "any",
    "asin",
    "atan",
    "atan2",
    "avg",
    "ceil",
    "coalesce",
    "collect",
    "cos",
    "cot",
    "count",
    "degrees",
    "e",
    "endNode",
    "exists",
    "exp",
    "extract",
    "filter",
    "floor",
    "haversin",
    "head",
    "id",
    "keys",
    "labels",
    "last",
    "left",
    "length",
    "log",
    "log10",
    "lTrim",
    "max",
    "min",
    "nodes",
    "none",
    "percentileCont",
    "percentileDisc",
    "pi",
    "distance",
    "point",
    "radians",
    "rand",
    "range",
    "reduce",
    "relationships",
    "replace",
    "reverse",
    "right",
    "round",
    "rTrim",
    "shortestPath",
    "sign",
    "sin",
    "single",
    "size",
    "split",
    "sqrt",
    "startNode",
    "stdDev",
    "stdDevP",
    "substring",
    "sum",
    "tail",
    "tan",
    "timestamp",
    "toBoolean",
    "toFloat",
    "toInteger",
    "toLower",
    "toString",
    "toUpper",
    "properties",
    "trim",
    "type",
]

neo4j_user_defined_functions = [
    "date",
    "date.realtime",
    "date.statement",
    "date.transaction",
    "date.truncate",
    "datetime",
    "datetime.fromepoch",
    "datetime.fromepochmillis",
    "datetime.realtime",
    "datetime.statement",
    "datetime.transaction",
    "datetime.truncate",
    "duration",
    "duration.between",
    "duration.inDays",
    "duration.inMonths",
    "duration.inSeconds",
    "localdatetime",
    "localdatetime.realtime",
    "localdatetime.statement",
    "localdatetime.transaction",
    "localdatetime.truncate",
    "localtime",
    "localtime.realtime",
    "localtime.statement",
    "localtime.transaction",
    "localtime.truncate",
    "randomUUID",
    "time",
    "time.realtime",
    "time.statement",
    "time.transaction",
    "time.truncate"
]


def word_list(words, token_type):
    return list(reversed(sorted((word.replace(" ", r"\s+") + r"\b", token_type) for word in words)))


def symbol_list(symbols, token_type):
    return list(reversed(sorted(("".join("\\" + ch for ch in symbol), token_type) for symbol in symbols)))


class CypherLexer(RegexLexer):
    """
    For `Cypher Query Language
    <https://neo4j.com/docs/cypher-refcard/current/>`_

    For the Cypher version in Neo4j 3.4
    """
    name = 'Cypher'
    aliases = ['cypher']
    filenames = ['*.cypher', '*.cyp']

    flags = re.IGNORECASE | re.MULTILINE | re.UNICODE

    tokens = {

        'root': [
            include('strings'),
            include('comments'),
            include('keywords'),
            include('pseudo-keywords'),
            (r'[,;]', Punctuation),
            include('labels'),
            include('operators'),
            include('expressions'),
            include('whitespace'),
            (r'\(', Punctuation, 'in-()'),
            (r'\[', Punctuation, 'in-[]'),
            (r'\{', Punctuation, 'in-{}'),
        ],
        'in-()': [
            include('strings'),
            include('comments'),
            include('keywords'),        # keywords used in FOREACH
            (r'[,|]', Punctuation),
            include('labels'),
            include('operators'),
            include('expressions'),
            include('whitespace'),
            (r'\(', Punctuation, '#push'),
            (r'\)\s*<?-+>?\s*\(', Punctuation),
            (r'\)\s*<?-+\s*\[', Punctuation, ('#pop', 'in-[]')),
            (r'\)', Punctuation, '#pop'),
            (r'\[', Punctuation, 'in-[]'),
            (r'\{', Punctuation, 'in-{}'),
        ],
        'in-[]': [
            include('strings'),
            include('comments'),
            (r'WHERE\b', Keyword),      # used in list comprehensions
            (r'[,|]', Punctuation),
            include('labels'),
            include('operators'),
            include('expressions'),
            include('whitespace'),
            (r'\(', Punctuation, 'in-()'),
            (r'\[', Punctuation, '#push'),
            (r'\]\s*-+>?\s*\(', Punctuation, ('#pop', 'in-()')),
            (r'\]', Punctuation, '#pop'),
            (r'\{', Punctuation, 'in-{}'),
        ],
        'in-{}': [
            include('strings'),
            include('comments'),
            (r'[,:]', Punctuation),
            include('operators'),
            include('expressions'),
            include('whitespace'),
            (r'\(', Punctuation, 'in-()'),
            (r'\[', Punctuation, 'in-[]'),
            (r'\{', Punctuation, '#push'),
            (r'\}', Punctuation, '#pop'),
        ],

        'comments': [
            (r'^.*//.*\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline-comments'),
        ],
        'multiline-comments': [
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^/*]+', Comment.Multiline),
            (r'[/*]', Comment.Multiline)
        ],

        'strings': [
            # TODO: highlight escape sequences
            (r"'(?:\\[bfnrt\"'\\]|\\u[0-9A-Fa-f]{4}|\\U[0-9A-Fa-f]{8}|[^\\'])*'", String),
            (r'"(?:\\[bfnrt\'"\\]|\\u[0-9A-Fa-f]{4}|\\U[0-9A-Fa-f]{8}|[^\\"])*"', String),
        ],

        'keywords': word_list(cypher_keywords, Keyword),
        'pseudo-keywords': word_list(cypher_pseudo_keywords, Keyword),

        'labels': [
            (r'(:)(\s*)(`(?:``|[^`])+`)', bygroups(Punctuation, Whitespace, Name.Label)),
            (r'(:)(\s*)([A-Za-z_][0-9A-Za-z_]*)', bygroups(Punctuation, Whitespace, Name.Label)),
        ],

        'operators': (word_list(cypher_operator_words, Operator) +
                      symbol_list(cypher_operator_symbols, Operator)),

        'expressions': [
            include('procedures'),
            include('functions'),
            include('constants'),
            include('aliases'),
            include('variables'),
            include('parameters'),
            include('numbers'),
        ],
        'procedures': [
            (r'(CALL)(\s+)([A-Za-z_][0-9A-Za-z_\.]*)', bygroups(Keyword, Whitespace, Name.Function)),
        ],
        'functions': [
            (r'([A-Za-z_][0-9A-Za-z_\.]*)(\s*)(\()', bygroups(Name.Function, Whitespace, Punctuation), "in-()"),
        ],
        'aliases': [
            (r'(AS)(\s+)(`(?:``|[^`])+`)', bygroups(Keyword, Whitespace, Name.Variable)),
            (r'(AS)(\s+)([A-Za-z_][0-9A-Za-z_]*)', bygroups(Keyword, Whitespace, Name.Variable)),
        ],
        'variables': [
            (r'`(?:``|[^`])+`', Name.Variable),
            (r'[A-Za-z_][0-9A-Za-z_]*', Name.Variable),
        ],
        'parameters': [
            (r'(\$)(`(?:``|[^`])+`)', bygroups(Punctuation, Name.Variable.Global)),
            (r'(\$)([A-Za-z_][0-9A-Za-z_]*)', bygroups(Punctuation, Name.Variable.Global)),
        ],
        'constants': word_list(cypher_constants, Name.Constant),
        'numbers': [
            (r'[0-9]*\.[0-9]*(e[+-]?[0-9]+)?', Number.Float),
            (r'[0-9]+e[+-]?[0-9]+', Number.Float),
            (r'[0-9]+', Number.Integer),
        ],

        'whitespace': [
            (r'\s+', Whitespace),
        ],

    }

    def get_statements(self, text):
        """ Split the text into statements delimited by semicolons and
        yield each statement in turn. Yielded statements are stripped
        of both leading and trailing whitespace. Empty statements are
        skipped.
        """
        fragments = []
        for index, token_type, value in self.get_tokens_unprocessed(text):
            if token_type == Punctuation and value == ";":
                statement = "".join(fragments).strip()
                fragments[:] = ()
                if statement:
                    yield statement
            else:
                fragments.append(value)
        statement = "".join(fragments).strip()
        if statement:
            yield statement
