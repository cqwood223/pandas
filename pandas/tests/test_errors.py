# -*- coding: utf-8 -*-

import pytest
from warnings import catch_warnings, simplefilter
import pandas  # noqa
import pandas as pd
from pandas.errors import AbstractMethodError
import pandas.util.testing as tm


@pytest.mark.parametrize(
    "exc", ['UnsupportedFunctionCall', 'UnsortedIndexError',
            'OutOfBoundsDatetime',
            'ParserError', 'PerformanceWarning', 'DtypeWarning',
            'EmptyDataError', 'ParserWarning', 'MergeError'])
def test_exception_importable(exc):
    from pandas import errors
    e = getattr(errors, exc)
    assert e is not None

    # check that we can raise on them
    with pytest.raises(e):
        raise e()


def test_catch_oob():
    from pandas import errors

    try:
        pd.Timestamp('15000101')
    except errors.OutOfBoundsDatetime:
        pass


def test_error_rename():
    # see gh-12665
    from pandas.errors import ParserError
    from pandas.io.common import CParserError

    try:
        raise CParserError()
    except ParserError:
        pass

    try:
        raise ParserError()
    except CParserError:
        pass

    with catch_warnings(record=True):
        simplefilter("ignore")
        try:
            raise ParserError()
        except pd.parser.CParserError:
            pass


class Foo(object):
    @classmethod
    def classmethod(cls):
        raise AbstractMethodError(cls, methodtype='classmethod')

    @property
    def property(self):
        raise AbstractMethodError(self, methodtype='property')

    def method(self):
        raise AbstractMethodError(self)


def test_AbstractMethodError_classmethod():
    xpr = "This classmethod must be defined in the concrete class Foo"
    with tm.assert_raises_regex(AbstractMethodError, xpr):
        Foo.classmethod()

    xpr = "This property must be defined in the concrete class Foo"
    with tm.assert_raises_regex(AbstractMethodError, xpr):
        Foo().property

    xpr = "This method must be defined in the concrete class Foo"
    with tm.assert_raises_regex(AbstractMethodError, xpr):
        Foo().method()
