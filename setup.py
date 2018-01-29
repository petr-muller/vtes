"""VtES game logger"""

from setuptools import setup, find_packages

setup(
    name="vtes",
    version="0.0.0",
    description="A VtES game logger",
    # long_description=
    # url=
    author="Petr Muller",
    author_email="afri@afri.cz",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Other Audience",
        "Topic :: Games/Entertainment :: Board Games",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="ccg vtes",
    packages=find_packages(exclude=["tests"]),
    setup_requires=['pytest-runner', 'pytest-bdd', 'pytest-pylint', 'pytest-mypy', 'pytest-cov',
                    'pyfakefs'],
    tests_require=['pytest', 'pylint', 'mypy'],
    install_requires=[],
    entry_points={'console_scripts': ['vtes=vtes.run:main']}
)
