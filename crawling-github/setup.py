from setuptools import setup

setup(
    name='crawling-github',
    packages=['crawler'],
    include_package_data=True,
    install_requires=[
        'urllib3',
        'requests',
        'certifi',
        'chardet',
        'idna',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
