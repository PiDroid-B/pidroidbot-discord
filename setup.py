#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Setup dot py."""
# Future
from __future__ import absolute_import, print_function

# Standard Library
# import re
from glob import glob
from os.path import basename, dirname, join, splitext

# Third Party
from setuptools import find_packages, setup


def read(*names, **kwargs):
    """Read description files."""
    path = join(dirname(__file__), *names)
    with open(path, encoding=kwargs.get("encoding", "utf8")) as fh:
        return fh.read()


# previous approach used to ignored badges in PyPI long description
# long_description = '{}\n{}'.format(
#     re.compile(
#         '^.. start-badges.*^.. end-badges',
#         re.M | re.S,
#         ).sub(
#             '',
#             read('README.rst'),
#             ),
#     re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read(join('docs', 'CHANGELOG.rst')))
#     )

long_description = "{}".format(read("README.rst"))

setup(
    name="pidroidbot-discord",
    description="A new friend to manage your discord server",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="CC BY-NC-SA 4.0",
    author="PiDroid-B",
    author_email="pidroid.b@gmail.com",
    url="https://github.com/PiDroid-B/pidroidbot-discord",
    packages=find_packages("pidroidbot_discord"),
    package_dir={"": "pidroidbot_discord"},
    py_modules=[splitext(basename(i))[0] for i in glob("pidroidbot_discord/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        # 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        # 'License :: OSI Approved :: MIT License',
        "License :: Other/Proprietary License",
        # 'Natural Language :: English',
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Communications :: Chat",
    ],
    project_urls={
        "webpage": "https://github.com/PiDroid-B/pidroidbot-discord",
        "Documentation": "https://pidroid-b.github.io/pidroidbot-discord/",
        # 'Changelog': 'https://github.com/joaomcteixeira/python-project-skeleton/blob/master/docs/CHANGELOG.rst',
        # 'Issue Tracker': 'https://github.com/joaomcteixeira/python-project-skeleton/issues',
        # 'Discussion Forum': 'https://github.com/joaomcteixeira/python-project-skeleton/discussions',
    },
    keywords=[
        # 'ci', 'continuous-integration', 'project-template',
        # 'project-skeleton', 'sample-project',
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires=">=3.6, <3.9",
    install_requires=[
        # 'matplotlib>=3',
        # 'click',
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        #   'pytest-runner',
        #   'setuptools_scm>=3.3.1',
    ],
    entry_points={
        "console_scripts": [
            "pidroidbot-discord = pidroidbot_discord:main",
        ]
        #
    },
    # cmdclass={'build_ext': optional_build_ext},
    # ext_modules=[
    #    Extension(
    #        splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
    #        sources=[path],
    #        include_dirs=[dirname(path)]
    #    )
    #    for root, _, _ in os.walk('src')
    #    for path in glob(join(root, '*.c'))
    # ],
)
