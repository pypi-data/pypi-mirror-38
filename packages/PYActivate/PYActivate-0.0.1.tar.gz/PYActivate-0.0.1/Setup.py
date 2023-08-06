from setuptools import setup

README = open('README.txt', 'r').read()

setup(
    name = 'PYActivate',
    version = '0.0.1',
    description = 'Python library for Marshall Activation Protocol',
    long_description = README,
    long_description_content_type = 'text',
    author = 'Ethan Marshall',
    author_email = '',
    url = 'https://github.com/CodeNinja16/MAP',
    packages = ['PYActivate'],
    entry_points = {},
    install_requires = {},
    keywords = ['python', 'activation', 'monetisation'],
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
