"""
OpenWrt packages
==================

This module provides tools to manage OpenWrt packages
and repositories.

"""
from __future__ import with_statement

from fabric.api import hide, run, settings

from fabtools.utils import run_as_root


def pkg_manager():
    return 'opkg'


def update_index(quiet=True):
    """
    Update packages definitions.
    """

    manager = pkg_manager()
    if quiet:
        with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
            run_as_root("%(manager)s update" % locals())
    else:
        run_as_root("%(manager)s update" % locals())


def upgrade():
    """
    Upgrade all packages.
    """
    raise NotImplementedError()


def is_installed(pkg_name):
    """
    Check if a package is installed.
    """

    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        manager = pkg_manager()
        res = run('%(manager)s list-installed | grep -i "%(pkg_name)s -"' % locals())
        return res.succeeded


def install(packages, update=False, options=None):
    """
    Install one or more packages.

    If *update* is ``True``, the package definitions will be updated
    first, using :py:func:`~fabtools.openwrt.update_index`.

    Extra *options* may be passed to ``opkg`` if necessary.

    Example::

        import fabtools

        # Update index, then install a single package
        fabtools.openwrt.install('mongodb', update=True)

        # Install multiple packages
        fabtools.openwrt.install([
            'mongodb',
            'python-pymongo',
        ])

    """
    manager = pkg_manager()
    if update:
        update_index()
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = " ".join(options)
    cmd = '%(manager)s install %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)


def uninstall(packages, options=None):
    """
    Remove one or more packages.

    Extra *options* may be passed to ``opkg`` if necessary.
    """
    manager = pkg_manager()
    if options is None:
        options = []
    if not isinstance(packages, basestring):
        packages = " ".join(packages)
    options = " ".join(options)
    cmd = '%(manager)s remove %(options)s %(packages)s' % locals()
    run_as_root(cmd, pty=False)


def uci_commit():
    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        run('uci commit')


def uci_set(configs, commit=True):
    """Set config with uci tools"""

    if isinstance(configs, basestring):
        configs = [configs]

    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        for config in configs:
            run("uci set %s" % config)

    if commit:
        uci_commit()
