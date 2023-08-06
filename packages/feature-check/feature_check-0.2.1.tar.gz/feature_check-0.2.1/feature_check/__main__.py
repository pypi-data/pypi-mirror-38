#!/usr/bin/python
#
# Copyright (c) 2018  Peter Pentchev
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

""" Query a program's list of features. """

from __future__ import print_function

import argparse
import sys

from . import defs
from . import expr as fexpr
from . import obtain

try:
    import simplejson as js
except ImportError:
    import json as js  # type: ignore

try:
    from typing import Dict, Optional

    _TYPING_USED = [Dict, Optional]
except ImportError:
    _TYPING_USED = []


class Config(object):
    # pylint: disable=too-few-public-methods
    """ Runtime configuration for this program. """

    def __init__(self, args):
        # type: (Config, argparse.Namespace) -> None
        """ Initialize a config object. """
        self.args = args
        self.program = '(unknown)'
        self.mode = '(unknown)'
        self.feature = '(unknown)'
        self.ast = None  # type: Optional[fexpr.Expr]


def version():
    # type: () -> None
    """
    Display program version information.
    """
    print('feature-check {ver}'.format(ver=defs.VERSION_STRING))


def features():
    # type: () -> None
    """
    Display program features information.
    """
    print('{prefix}feature-check={ver} single=1.0 list=1.0 simple=1.0'
          .format(prefix=defs.DEFAULT_PREFIX, ver=defs.VERSION_STRING))


def output_tsv(data):
    # type: (Dict[str, str]) -> None
    """ List the obtained features as tab-separated name/value pairs. """
    for feature in sorted(data.keys()):
        print('{feature}\t{version}'
              .format(feature=feature, version=data[feature]))


def output_json(data):
    # type: (Dict[str, str]) -> None
    """ List the obtained features as a JSON object. """
    print(js.dumps(data, sort_keys=True, indent='  '))


OUTPUT = {
    'tsv': output_tsv,
    'json': output_json,
}


def process_list(cfg, data):
    # type: (Config, Dict[str, str]) -> None
    """ List the obtained features using the specified method. """
    OUTPUT[cfg.args.output_format](data)


def process_single(cfg, data):
    # type: (Config, Dict[str, str]) -> None
    """ Check whether a single feature is present. """
    if cfg.feature in data:
        if cfg.args.display_version:
            print(data[cfg.feature])
        sys.exit(0)
    else:
        sys.exit(1)


def process_expr(cfg, data):
    # type: (Config, Dict[str, str]) -> None
    """ Evaluate an expression against the obtained features list. """
    assert cfg.ast is not None
    res = cfg.ast.evaluate(data)
    assert isinstance(res, fexpr.ResultBool), \
        'how to handle a {t} object?'.format(t=type(res).__name__)
    sys.exit(0 if res.value else 1)


PROCESS = {
    'list': process_list,
    'single': process_single,
    'expr': process_expr,
}


def main():
    # type: () -> None
    '''
    The main routine: parse command-line arguments, do things.
    '''
    parser = argparse.ArgumentParser(
        prog='feature-check',
        usage='''
    feature-check [-v] [-O optname] [-P prefix] program feature
    feature-check [-O optname] [-P prefix] program feature op version
    feature-check [-O optname] [-o json|tsv] [-P prefix] -l program
    feature-check -V | -h''')
    parser.add_argument('-V', '--version', action='store_true',
                        help='display program version information and exit')
    parser.add_argument('--features', action='store_true',
                        help='display supported features and exit')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list the features supported by a program')
    parser.add_argument('-O', '--option-name', type=str,
                        default=defs.DEFAULT_OPTION,
                        help='the query-features option to pass')
    parser.add_argument('-o', '--output-format',
                        default=defs.DEFAULT_OUTPUT_FMT,
                        choices=sorted(OUTPUT.keys()),
                        help='specify the output format for the list')
    parser.add_argument('-P', '--features-prefix', type=str,
                        default=defs.DEFAULT_PREFIX,
                        help='the features prefix in the program output')
    parser.add_argument('-v', '--display-version', action='store_true',
                        help='display the feature version')
    parser.add_argument('args', nargs='*',
                        help='the program and features to test')

    args = parser.parse_args()
    if args.version:
        version()
        sys.exit(0)
    if args.features:
        features()
        sys.exit(0)

    cfg = Config(args)

    if args.list:
        if len(args.args) != 1:
            parser.error('No program specified')
        cfg.program = args.args.pop(0)
        cfg.mode = 'list'
    else:
        if len(args.args) < 2:
            parser.error('No program or feature specified')
        cfg.program = args.args.pop(0)
        cfg.feature = ' '.join(args.args)
        m_single = fexpr.parse_single(cfg.feature)
        m_simple = fexpr.parse_simple(cfg.feature)
        if m_single:
            cfg.mode = 'single'
        elif m_simple:
            cfg.mode = 'expr'
            cfg.ast = m_simple
        else:
            parser.error('Only querying a single feature supported so far')

    try:
        data = obtain.obtain_features(cfg.program, cfg.args.option_name,
                                      cfg.args.features_prefix)
    except obtain.ObtainError as exc:
        sys.exit(exc.code)

    PROCESS[cfg.mode](cfg, data)


if __name__ == '__main__':
    main()
