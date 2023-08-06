#!/usr/bin/env python
import os
import mac_colors
import public
import travis_failed

"""
works only if path basename same as github/travis repo name
https://travis-ci.org/owner/repo
path/to/repo
"""


@public.add
def repos():
    """return list of travis repos"""
    cmd = "travis repos -a --skip-completion-check --skip-version-check"
    return os.popen(cmd).read().splitlines()


@public.add
def failed_repos():
    """return list of failed travis repos"""
    return travis_failed.failed_repos()


@public.add
def mdfind():
    """return list of travis repos paths"""
    q = []
    for fullname in repos():
        q.append('kMDItemDisplayName==%s' % os.path.basename(fullname))
    matches = os.popen("mdfind '%s'" % " || ".join(q)).read().splitlines()
    paths = []
    for path in matches:
        if os.path.exists(os.path.join(path, ".git")):
            paths.append(path)
    return list(sorted(paths))


@public.add
def tag():
    """set Finder tags (`red` - failed, `none` - passed)"""
    passed = []
    failed = []
    paths = mdfind()
    for fullname in failed_repos():
        name = os.path.basename(fullname)
        failed += list(filter(lambda path: name == os.path.basename(path), paths))
    passed = list(set(paths) - set(failed))
    mac_colors.none(passed)
    mac_colors.red(failed)
    return passed, failed
