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
Version string parsing for the feature-check Python library.
"""

import re

try:
    from typing import Any, Callable, List, Optional, Tuple

    _TYPING_USED = [Any, Callable, List, Optional, Tuple]
except ImportError:
    _TYPING_USED = []


REX = {
    'var': r'[A-Za-z0-9_-]+',
    'value': r'[A-Za-z0-9.]+',
    'op': r'(?: < | <= | = | >= | > | lt | le | eq | ge | gt )',
    'num_alpha': r'(?P<num> [0-9]* ) (?P<alpha> .*)',
}

REX_COMP = {
    name: re.compile(expr + '$', re.X) for name, expr in REX.items()
}


def _version_split_num_alpha(ver):
    # type: (str) -> Tuple[str, str]
    """
    Split a version component into a numeric and an alphanumeric part,
    e.g. "2a" is split into ('2', 'a').
    """
    match = REX_COMP['num_alpha'].match(ver)
    assert match is not None
    data = match.groupdict()
    return data['num'], data['alpha']


def _version_compare_split_empty(spl_a, spl_b):
    # type: (List[str], List[str]) -> Optional[int]
    """
    Check if any of the split version numbers is empty.
    """
    if not spl_a:
        if not spl_b:
            return 0
        if _version_split_num_alpha(spl_b[0])[0] == '':
            return 1
        return -1
    if not spl_b:
        if _version_split_num_alpha(spl_a[0])[0] == '':
            return -1
        return 1

    return None


def _version_compare_split_comp(comp_a, comp_b, conv):
    # type: (str, str, Callable[[str], Any]) -> Optional[int]
    """
    Compare a single component of split version numbers.
    """
    if comp_a != '':
        if comp_b != '':
            if conv(comp_a) < conv(comp_b):
                return -1
            if conv(comp_a) > conv(comp_b):
                return 1
        else:
            return 1
    elif comp_b != '':
        return -1

    return None


def _version_compare_split(spl_a, spl_b):
    # type: (List[str], List[str]) -> int
    """
    Compare two version numbers already split into lists of version
    number components.
    Returns -1, 0, or 1 for the first version being less than, equal to,
    or greater than the second one.
    """
    res = _version_compare_split_empty(spl_a, spl_b)
    if res is not None:
        return res

    (first_a, first_b) = (spl_a.pop(0), spl_b.pop(0))
    (num_a, rem_a) = _version_split_num_alpha(first_a)
    assert num_a != '' or rem_a != '', 'could not split ' + first_a
    (num_b, rem_b) = _version_split_num_alpha(first_b)
    assert num_b != '' or rem_b != '', 'could not split ' + first_b

    res = _version_compare_split_comp(num_a, num_b, int)
    if res is not None:
        return res

    res = _version_compare_split_comp(rem_a, rem_b, lambda s: s)
    if res is not None:
        return res

    return _version_compare_split(spl_a, spl_b)


def version_compare(ver_a, ver_b):
    # type: (str, str) -> int
    """
    Compare two version numbers as strings.
    Returns -1, 0, or 1 for the first version being less than, equal to,
    or greater than the second one.
    """
    return _version_compare_split(ver_a.split('.'), ver_b.split('.'))
