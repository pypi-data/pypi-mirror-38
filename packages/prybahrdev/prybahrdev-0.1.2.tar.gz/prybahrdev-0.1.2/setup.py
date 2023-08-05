"""
# ======================================================================================================================
#
# Copyright (c) 2018 nfwatson.com
#
# REPO           :  ...
# FILE           :  ...
# LICENSE        :  MIT
#
# ======================================================================================================================

...

# ======================================================================================================================
"""

from setuptools import setup, find_packages

# TODO:  extract long-description additional metadata from README.md or similar

setup(
    #
    # -- basics

    name='prybahrdev',
    license='MIT',
    description='prybahrdev ...',
    long_description='prybahrdev (long ...)',
    author='Dev@NFWatson.Com',
    author_email='dev@nfwatson.com',
    url='https://TBD-3BBA9E5B.nfwatson.com/TBD-3BBA9E5B',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    # DO_NOT:  py_modules=[],  # ... required only if single-file top-level modules are distributed

    include_package_data=False,
    # package_data=[...],
    # zip_safe=False,

    # -- package version ... derived from VCS

    # DO_NOT:  version='x.y.z',  # ... but instead ...
    setup_requires=['setuptools_scm'],
    use_scm_version={'root': '.', 'relative_to': __file__},

    # -- straight dependencies

    install_requires=[
        # 'requests',
        # 'boltons',
    ],

    # -- extras' dependencies

    extras_require={
        # 'opt1', ['bla-bla'],
        # 'opt2', ['blah-blah'],
    },

    # -- package entry points

    entry_points={
        # ...
    },

    # -- distributed scripts

    # scripts=[...],

    # -- classifiers, keywords

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        # ...
    ],

    keywords=[
        # ...
    ],
)

# END OF FILE.
