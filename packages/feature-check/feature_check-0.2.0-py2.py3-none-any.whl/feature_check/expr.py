# Copyright (c) 2018  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"""
Expression evaluation for the feature-check Python library.
"""


import abc
import re

from typing import Callable, Dict, List, Optional, Type

import six

from . import version as fver


_TYPING_USED = (Dict, Optional, Type)


class Result(object):
    # pylint: disable=too-few-public-methods
    """
    The base class for an expression result.
    """
    def __init__(self):
        # type: (Result) -> None
        """
        Initialize a Result object... do nothing.
        """
        pass


class ResultBool(Result):
    # pylint: disable=too-few-public-methods
    """
    A boolean result of an expression; the "value" member is boolean.
    """
    def __init__(self, value):
        # type: (ResultBool, bool) -> None
        """
        Initialize a ResultBool object with the specified value.
        """
        super(ResultBool, self).__init__()
        self.value = value

    def __str__(self):
        # type: (ResultBool) -> str
        return 'ResultBool: {value}'.format(value=self.value)


class ResultVersion(Result):
    # pylint: disable=too-few-public-methods
    """
    A version number as a result of an expression; the "value" member is
    the version number string.
    """
    def __init__(self, value):
        # type: (ResultVersion, str) -> None
        """
        Initialize a ResultVersion object with the specified value.
        """
        super(ResultVersion, self).__init__()
        self.value = value

    def __str__(self):
        # type: (ResultVersion) -> str
        return 'ResultVersion: {value}'.format(value=self.value)


@six.add_metaclass(abc.ABCMeta)
class Expr(object):
    # pylint: disable=too-few-public-methods
    """
    The (pretty much abstract) base class for an expression.
    """
    def __init__(self):
        # type: (Expr) -> None
        """
        Initialize an expression object... do nothing.
        """
        pass

    @abc.abstractmethod
    def evaluate(self, data):
        # type: (Expr, Dict[str, str]) -> Result
        """
        Overridden in actual expression classes to evaluate
        the expression and return a Result object.
        """
        raise NotImplementedError('{t}.evaluate() must be overrridden'
                                  .format(t=type(self).__name__))


class ExprFeature(Expr):
    # pylint: disable=too-few-public-methods
    """
    An expression that returns a program feature name as a string.
    """
    def __init__(self, name):
        # type: (ExprFeature, str) -> None
        """
        Initialize the expression with the specified feature name.
        """
        super(ExprFeature, self).__init__()
        self.name = name

    def evaluate(self, data):
        # type: (ExprFeature, Dict[str, str]) -> ResultVersion
        """
        Look up the feature and return a ResultVersion object with the result.
        """
        return ResultVersion(value=data[self.name])


class ExprVersion(Expr):
    # pylint: disable=too-few-public-methods
    """
    An expression that returns a version number for a feature.
    """
    def __init__(self, value):
        # type: (ExprVersion, str) -> None
        """
        Initialize the expression with the specified version string.
        """
        super(ExprVersion, self).__init__()
        self.value = value

    def evaluate(self, data):
        # type: (ExprVersion, Dict[str, str]) -> ResultVersion
        """
        Return the version number as a ResultVersion object.
        """
        return ResultVersion(value=self.value)


BoolOpFunction = Callable[[List[Result]], bool]


class BoolOp(object):
    """ A two-argument boolean operation. """

    def __init__(self,   # type: BoolOp
                 args,   # type: List[Type[Result]]
                 action  # type: BoolOpFunction
                 ):      # type: (...) -> None
        """ Initialize an operation object. """
        self._args = args
        self._action = action

    @property
    def args(self):
        # type: (BoolOp) -> List[Type[Result]]
        """ Return the argument types of the operation. """
        return self._args

    @property
    def action(self):
        # type: (BoolOp) -> BoolOpFunction
        """ Return the function that performs the operation. """
        return self._action


def _def_op_bool_ver(check):
    # type: (Callable[[int], bool]) -> BoolOpFunction

    def _op_bool_ver(args):
        # type: (List[Result]) -> bool
        """ Check whether the arguments are in the expected relation. """
        assert len(args) == 2
        assert isinstance(args[0], ResultVersion)
        assert isinstance(args[1], ResultVersion)
        return check(fver.version_compare(args[0].value, args[1].value))

    return _op_bool_ver


class ExprOp(Expr):
    # pylint: disable=too-few-public-methods
    """
    A two-argument operation expression.
    """

    OPS = {
        'lt': BoolOp(
            args=[ResultVersion, ResultVersion],
            action=_def_op_bool_ver(lambda res: res < 0),
        ),
        'le': BoolOp(
            args=[ResultVersion, ResultVersion],
            action=_def_op_bool_ver(lambda res: res <= 0),
        ),
        'eq': BoolOp(
            args=[ResultVersion, ResultVersion],
            action=_def_op_bool_ver(lambda res: res == 0),
        ),
        'ge': BoolOp(
            args=[ResultVersion, ResultVersion],
            action=_def_op_bool_ver(lambda res: res >= 0),
        ),
        'gt': BoolOp(
            args=[ResultVersion, ResultVersion],
            action=_def_op_bool_ver(lambda res: res > 0),
        ),
    }

    SYNONYMS = {
        '<':  'lt',
        '<=': 'le',
        '=':  'eq',
        '>=': 'ge',
        '>':  'gt',
    }

    for (k, v) in SYNONYMS.items():
        OPS[k] = OPS[v]

    def __init__(self, op_name, args):
        # type: (ExprOp, str, List[Expr]) -> None
        """
        Initialize an expression with the specified operation and
        arguments (Expr objects in their own right).
        """
        super(ExprOp, self).__init__()
        if op_name not in self.OPS:
            raise ValueError('op')

        # TODO: handle all, any
        if len(args) != len(self.OPS[op_name].args):
            raise ValueError('args')
        if any(not isinstance(arg, Expr) for arg in args):
            raise ValueError('args')

        self.op_name = op_name
        self.args = args

    def evaluate(self, data):
        # type: (ExprOp, Dict[str, str]) -> ResultBool
        """
        Evaluate the expression over the specified data.
        """
        operation = self.OPS[self.op_name]
        args = [expr.evaluate(data) for expr in self.args]

        # TODO: handle all, any
        for (idx, value) in enumerate(args):
            if not isinstance(value, operation.args[idx]):
                raise ValueError('{op} argument {idx}'.format(op=self.op_name,
                                                              idx=idx))

        return ResultBool(value=operation.action(args))


def parse_single(expr):
    # type: (str) -> Optional[str]
    """
    Parse a trivial "feature-name" 'expression'.

    If the expression is a valid feature name, return it.
    Otherwise, return None.
    """
    m_single = re.match(fver.REX['var'] + '$', expr)
    if not m_single:
        return None

    return expr


def parse_simple(expr):
    # type: (str) -> Optional[Expr]
    """
    Parse a simple "feature-name op version" expression.

    If the expression is valid, return an `Expr` object corresponding
    to the specified check.  Use this object's `evaluate()` method and
    pass a features dictionary as returned by the `obtain_features()`
    function to get a `Result` object; for simple expressions it will be
    a `ResultBool` object with a boolean `value` member.

        from feature_check import expr as fexpr
        from feature_check import obtain as fobtain

        data = fobtain.obtain_features("timelimit");
        expr = fexpr.parse_simple("subsecond > 0")
        print(expr.evaluate(data).value)
    """
    m_simple = re.match(
        r'''
            (?P<var> {var} ) \s*
            (?P<op> {op} ) \s*
            (?P<value> {value} )
            $
        '''.format(var=fver.REX['var'],
                   op=fver.REX['op'],
                   value=fver.REX['value']),
        expr, re.X)
    if not m_simple:
        return None

    data = m_simple.groupdict()
    return ExprOp(op_name=data['op'], args=[
        ExprFeature(name=data['var']),
        ExprVersion(value=data['value']),
    ])
