import os
from setuptools import setup


setup(
    name = 'cocktail_model_lib',
    version = '0.0.3',
    author='Brandon Purvis',
    author_email='bpurvis.career@gmail.com',
    description='Library of tools for managing a database on cocktails.',
    license='MIT',
    keywords='cocktail sqlalchemy database',
    url='https://github.com/brandonPurvis/CocktailModelLib',
    packages=['cocktail_model_lib'],
    package_data={
        '': ['*.txt', '*.rst', '*.md'],
    },
    install_requires=[
        'SQLAlchemy',
        'marshmallow',
        'pytest',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
