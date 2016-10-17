#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Initially Generated By:
    python -m utool --tf setup_repo --repo=sandbox_utools --codedir=~/code --modname=sandbox_utools
"""
from __future__ import absolute_import, division, print_function, unicode_literals


def sandbox_utools_main():
    ignore_prefix = []
    ignore_suffix = []
    import utool as ut
    ut.main_function_tester('sandbox_utools', ignore_prefix, ignore_suffix)

if __name__ == '__main__':
    """
    Usage:
        python -m sandbox_utools <funcname>
    """
    print('Running sandbox_utools main')
    sandbox_utools_main()
