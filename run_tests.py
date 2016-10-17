#!/usr/bin/env python2.7
"""
Initially Generated By:
    python -m utool --tf setup_repo --repo=sandbox_utools --codedir=~/code --modname=sandbox_utools --force-run_tests.py
"""
from __future__ import absolute_import, division, print_function
import sys
import utool as ut


def run_tests():
    # Build module list and run tests
    import sys
    ut.change_term_title('RUN sandbox_utools TESTS')
    exclude_doctests_fnames = set([
    ])
    exclude_dirs = [
        '_broken', 'old', 'tests', 'timeits',
        '_scripts', '_timeits', '_doc', 'notebook',
    ]
    dpath_list = ['sandbox_utools']
    doctest_modname_list = ut.find_doctestable_modnames(
        dpath_list, exclude_doctests_fnames, exclude_dirs)

    coverage = ut.get_argflag(('--coverage', '--cov',))
    if coverage:
        import coverage
        cov = coverage.Coverage(source=doctest_modname_list)
        cov.start()
        print('Starting coverage')

        exclude_lines = [
            'pragma: no cover',
            'def __repr__',
            'if self.debug:',
            'if settings.DEBUG',
            'raise AssertionError',
            'raise NotImplementedError',
            'if 0:',
            'if ut.VERBOSE',
            'if _debug:',
            'if __name__ == .__main__.:',
            'print(.*)',
        ]
        for line in exclude_lines:
            cov.exclude(line)

    for modname in doctest_modname_list:
        exec('import ' + modname, globals())
    module_list = [sys.modules[name] for name in doctest_modname_list]

    nPass, nTotal, failed_cmd_list = ut.doctest_module_list(module_list)

    if coverage:
        print('Stoping coverage')
        cov.stop()
        print('Saving coverage')
        cov.save()
        print('Generating coverage html report')
        cov.html_report()

    if nPass != nTotal:
        return 1
    else:
        return 0

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    retcode = run_tests()
    sys.exit(retcode)