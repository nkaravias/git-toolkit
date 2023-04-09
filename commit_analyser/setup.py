from setuptools import setup, find_packages

setup(
    name='commit_analyser',
    version='0.1',
    packages=find_packages(),
    test_suite='tests',
    install_requires=[
        'GitPython>=3.1.14',
        'pyyaml>=5.4.1'
    ],
    tests_require=[
        'pytest>=6.2.4',
        'coverage>=6.2.0'
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.4',
            'pytest-cov>=2.12.1'
        ]
    },
    entry_points={
        'console_scripts': [
            'commit-analyser=commit_analyser.cli:main'
        ]
    },
    cmdclass={
        'test': 'pytest'
    },
    setup_requires=[
        'coverage>=6.2.0'
    ],
    options={
        'coverage': {
            'include': ['commit_analyser/*'],
            'omit': ['tests/*']
        }
    }
)

