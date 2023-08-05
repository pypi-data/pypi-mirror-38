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

Some reference materials for setup.py:

    * https://blog.ionelmc.ro/2014/05/25/python-packaging/
    * http://andrewsforge.com/article/python-new-package-landscape/

# ======================================================================================================================
"""

from setuptools import setup, find_packages

# TODO:  extract long-description additional metadata from README.md or similar

setup(
    #
    # -- basics

    name='prybahr',
    license='MIT',
    description='prybahr ...',
    long_description='prybahr (long ...)',
    author='Dev@NFWatson.Com',
    author_email='dev@nfwatson.com',
    url='https://TBD-36A8DB87.nfwatson.com/TBD-36A8DB87',
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

    scripts=['scripts/eg_prybahr_script.py'],

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
