"""Setup file for handling packaging and distribution."""
from __future__ import absolute_import
from setuptools import setup, find_packages

__version__ = "0.7.3"

requirements = [
    "colored",
]

setup(
    name='patch_issue',
    version=__version__,
    description="",
    license="MIT",
    author="yakobu & shefer",
    author_email="ronenya4321@gmail.com",
    url="https://github.com/yakobu/patch_issue",
    keywords="patch",
    install_requires=requirements,
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    entry_points={},
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={'': ['*.xls', '*.xsd', '*.json', '*.css', '*.xml', '*.rst']},
    extras_require={
        'dev': [
            'property-manager',
            'attrdict',
            'mock',
            'flake8',
            'pytest',
            'pytest-cov',
        ],
    },
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
)
