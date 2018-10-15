from setuptools import setup

setup(
    name='crawling-github',
    packages=['crawler', 'GitHubAPI', 'twitter'],
    include_package_data=True,
    install_requires=[
        'wheel',
        'urllib3',
        'requests',
        'certifi',
        'chardet',
        'idna',
        'tweepy',
        'networkx'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
