from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

import templar

version = templar.__version__
dependencies = [
    'jinja2==2.8',
]

setup(
    name='templar',
    version=version,
    description='A static templating engine written in Python',
    url='https://github.com/albert12132/templar',
    author='Albert Wu',
    author_email='albert12132@gmail.com',
    license='MIT',
    keywords=['templating', 'static template', 'markdown'],
    packages=find_packages(exclude=['tests*']),
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'templar=templar.cli.templar:main',
            'markdown=templar.markdown:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)

