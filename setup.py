from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
# with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#     long_description = f.read()

dependencies = [
    'colorama',
]

setup(
    name='templar',
    version='1.3.1',
    description='A static templating engine written in Python',
    # long_description=long_description,
    url='https://github.com/albert12132/templar',
    author='Albert Wu',
    author_email='albert12132@gmail.com',
    license='MIT',
    keywords=['templating', 'static template', 'markdown'],
    packages=find_packages(exclude=['tests*']),
    install_requires=dependencies,
    package_data={
        'templar': ['config.py'],
    },
    entry_points={
        'console_scripts': [
            'templar=templar.__main__:main',
            'markdown=templar.markdown:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)

