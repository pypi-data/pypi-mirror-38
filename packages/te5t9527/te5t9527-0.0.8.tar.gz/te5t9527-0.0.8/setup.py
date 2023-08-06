from setuptools import setup, find_packages, Extension


setup(
    name = 'te5t9527',
    version = '0.0.8',
    description = 'test python publish by travis-ci',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/Secbone/py_publish_test',
    author = 'Secbone',
    author_email = 'secbone@gmail.com',
    packages = find_packages(exclude = ['tests']),
    python_requires = '>=3.5',
    setup_requires = [
        'setuptools',
    ],
    license = 'MIT',
    entry_points = {
        'console_scripts': [
            'te5t9527 = te5t9527.cli:main',
        ],
    },
)
