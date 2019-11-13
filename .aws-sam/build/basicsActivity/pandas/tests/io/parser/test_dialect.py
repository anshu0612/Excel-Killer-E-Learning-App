"""
Tests that dialects are properly handled during parsing
for all of the parsers defined in parsers.py
"""

import csv
from io import StringIO

import pytest

from pandas.errors import ParserWarning

from pandas import DataFrame
import pandas.util.testing as tm


@pytest.fixture
def custom_dialect():
    dialect_name = "weird"
    dialect_kwargs = dict(
        doublequote=False,
        escapechar="~",
        delimiter=":",
        skipinitialspace=False,
        quotechar="~",
        quoting=3,
    )
    return dialect_name, dialect_kwargs


def test_dialect(all_parsers):
    parser = all_parsers
    data = """\
label1,label2,label3
index1,"a,c,e
index2,b,d,f
"""

    dia = csv.excel()
    dia.quoting = csv.QUOTE_NONE
    df = parser.read_csv(StringIO(data), dialect=dia)

    data = """\
label1,label2,label3
index1,a,c,e
index2,b,d,f
"""
    exp = parser.read_csv(StringIO(data))
    exp.replace("a", '"a', inplace=True)
    tm.assert_frame_equal(df, exp)


def test_dialect_str(all_parsers):
    dialect_name = "mydialect"
    parser = all_parsers
    data = """\
fruit:vegetable
apple:broccoli
pear:tomato
"""
    exp = DataFrame({"fruit": ["apple", "pear"], "vegetable": ["broccoli", "tomato"]})

    with tm.with_csv_dialect(dialect_name, delimiter=":"):
        df = parser.read_csv(StringIO(data), dialect=dialect_name)
        tm.assert_frame_equal(df, exp)


def test_invalid_dialect(all_parsers):
    class InvalidDialect:
        pass

    data = "a\n1"
    parser = all_parsers
    msg = "Invalid dialect"

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(data), dialect=InvalidDialect)


@pytest.mark.parametrize(
    "arg",
    [None, "doublequote", "escapechar", "skipinitialspace", "quotechar", "quoting"],
)
@pytest.mark.parametrize("value", ["dialect", "default", "other"])
def test_dialect_conflict_except_delimiter(all_parsers, custom_dialect, arg, value):
    # see gh-23761.
    dialect_name, dialect_kwargs = custom_dialect
    parser = all_parsers

    expected = DataFrame({"a": [1], "b": [2]})
    data = "a:b\n1:2"

    warning_klass = None
    kwds = dict()

    # arg=None tests when we pass in the dialect without any other arguments.
    if arg is not None:
        if "value" == "dialect":  # No conflict --> no warning.
            kwds[arg] = dialect_kwargs[arg]
        elif "value" == "default":  # Default --> no warning.
            from pandas.io.parsers import _parser_defaults

            kwds[arg] = _parser_defaults[arg]
        else:  # Non-default + conflict with dialect --> warning.
            warning_klass = ParserWarning
            kwds[arg] = "blah"

    with tm.with_csv_dialect(dialect_name, **dialect_kwargs):
        with tm.assert_produces_warning(warning_klass):
            result = parser.read_csv(StringIO(data), dialect=dialect_name, **kwds)
            tm.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "kwargs,warning_klass",
    [
        (dict(sep=","), None),  # sep is default --> sep_override=True
        (dict(sep="."), ParserWarning),  # sep isn't default --> sep_override=False
        (dict(delimiter=":"), None),  # No conflict
        (dict(delimiter=None), None),  # Default arguments --> sep_override=True
        (dict(delimiter=","), ParserWarning),  # Conflict
        (dict(delimiter="."), ParserWarning),  # Conflict
    ],
    ids=[
        "sep-override-true",
        "sep-override-false",
        "delimiter-no-conflict",
        "delimiter-default-arg",
        "delimiter-conflict",
        "delimiter-conflict2",
    ],
)
def test_dialect_conflict_delimiter(all_parsers, custom_dialect, kwargs, warning_klass):
    # see gh-23761.
    dialect_name, dialect_kwargs = custom_dialect
    parser = all_parsers

    expected = DataFrame({"a": [1], "b": [2]})
    data = "a:b\n1:2"

    with tm.with_csv_dialect(dialect_name, **dialect_kwargs):
        with tm.assert_produces_warning(warning_klass):
            result = parser.read_csv(StringIO(data), dialect=dialect_name, **kwargs)
            tm.assert_frame_equal(result, expected)
