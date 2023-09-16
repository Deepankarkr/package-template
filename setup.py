#!/usr/bin/env python3

# Copyright (c) 2023 Kumar, Deepankar. All rights reserved.
# Use of this source code is governed by a license that can be
# found in the LICENSE file.

"""Cross-platform lib for process and system monitoring in Python."""

from __future__ import print_function

import contextlib
import glob
import io
import os
import platform
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import warnings


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    try:
        import setuptools
        from setuptools import Extension
        from setuptools import setup
    except ImportError:
        setuptools = None
        from distutils.core import Extension
        from distutils.core import setup
    try:
        from wheel.bdist_wheel import bdist_wheel
    except ImportError:
        if "CIBUILDWHEEL" in os.environ:
            raise
        bdist_wheel = None

HERE = os.path.abspath(os.path.dirname(__file__))

# ...so we can import _common.py and _compat.py
sys.path.insert(0, os.path.join(HERE, "psutil"))

def main():
    kwargs = dict(
        name='psutil',
        version=VERSION,
        cmdclass=cmdclass,
        description=__doc__ .replace('\n', ' ').strip() if __doc__ else '',
        long_description=get_long_description(),
        long_description_content_type='text/x-rst',
        keywords=[
            'ps', 'top', 'kill', 'free', 'lsof', 'netstat', 'nice', 'tty',
            'ionice', 'uptime', 'taskmgr', 'process', 'df', 'iotop', 'iostat',
            'ifconfig', 'taskset', 'who', 'pidof', 'pmap', 'smem', 'pstree',
            'monitoring', 'ulimit', 'prlimit', 'smem', 'performance',
            'metrics', 'agent', 'observability',
        ],
        author='Giampaolo Rodola',
        author_email='g.rodola@gmail.com',
        url='https://github.com/giampaolo/psutil',
        platforms='Platform Independent',
        license='BSD-3-Clause',
        packages=['psutil', 'psutil.tests'],
        ext_modules=get_extensions(),
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: Win32 (MS Windows)',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: BSD License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows :: Windows 10',
            'Operating System :: Microsoft :: Windows :: Windows 7',
            'Operating System :: Microsoft :: Windows :: Windows 8',
            'Operating System :: Microsoft :: Windows :: Windows 8.1',
            'Operating System :: Microsoft :: Windows :: Windows Server 2003',
            'Operating System :: Microsoft :: Windows :: Windows Server 2008',
            'Operating System :: Microsoft :: Windows :: Windows Vista',
            'Operating System :: Microsoft',
            'Operating System :: OS Independent',
            'Operating System :: POSIX :: AIX',
            'Operating System :: POSIX :: BSD :: FreeBSD',
            'Operating System :: POSIX :: BSD :: NetBSD',
            'Operating System :: POSIX :: BSD :: OpenBSD',
            'Operating System :: POSIX :: BSD',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX :: SunOS/Solaris',
            'Operating System :: POSIX',
            'Programming Language :: C',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries',
            'Topic :: System :: Benchmark',
            'Topic :: System :: Hardware :: Hardware Drivers',
            'Topic :: System :: Hardware',
            'Topic :: System :: Monitoring',
            'Topic :: System :: Networking :: Monitoring :: Hardware Watchdog',
            'Topic :: System :: Networking :: Monitoring',
            'Topic :: System :: Networking',
            'Topic :: System :: Operating System',
            'Topic :: System :: Systems Administration',
            'Topic :: Utilities',
        ],
    )
    if setuptools is not None:
        kwargs.update(
            python_requires=(
                ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*"),
            extras_require=extras_require,
            zip_safe=False,
        )
    success = False
    try:
        setup(**kwargs)
        success = True
    finally:
        cmd = sys.argv[1] if len(sys.argv) >= 2 else ''
        if not success and POSIX and \
                cmd.startswith(("build", "install", "sdist", "bdist",
                                "develop")):
            py3 = "3" if PY3 else ""
            if LINUX:
                pyimpl = "pypy" if PYPY else "python"
                if which('dpkg'):
                    missdeps("sudo apt-get install gcc %s%s-dev" %
                             (pyimpl, py3))
                elif which('rpm'):
                    missdeps("sudo yum install gcc %s%s-devel" % (pyimpl, py3))
                elif which('apk'):
                    missdeps("sudo apk add gcc %s%s-dev" % (pyimpl, py3))
            elif MACOS:
                print(hilite("XCode (https://developer.apple.com/xcode/) "
                             "is not installed", color="red"), file=sys.stderr)
            elif FREEBSD:
                if which('pkg'):
                    missdeps("pkg install gcc python%s" % py3)
                elif which('mport'):   # MidnightBSD
                    missdeps("mport install gcc python%s" % py3)
            elif OPENBSD:
                missdeps("pkg_add -v gcc python%s" % py3)
            elif NETBSD:
                missdeps("pkgin install gcc python%s" % py3)
            elif SUNOS:
                missdeps("sudo ln -s /usr/bin/gcc /usr/local/bin/cc && "
                         "pkg install gcc")


if __name__ == '__main__':
    main()
