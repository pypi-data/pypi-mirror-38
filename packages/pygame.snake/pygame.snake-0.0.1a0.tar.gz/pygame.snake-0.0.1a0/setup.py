from setuptools import find_packages, setup
from os import path


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    long_description = f.read()

version = __import__('snake').__version__

with open(path.join(path.abspath(path.dirname(__file__)), 'requirements.txt')) as f:
    requirements = f.readlines()


setup(
    name='pygame.snake',

    version=version,

    description='The super-simple pygame framework.',
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/Bottersnike/snake',

    author='Bottersnike',
    author_email='bottersnike237@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Games/Entertainment',
    ],

    keywords='engine python pygame',

    packages=find_packages(),
    install_requires=requirements,

    project_urls={
        'Wiki': 'https://github.com/Bottersnike/Snake/wiki',
        'Source': 'https://github.com/Bottersnike/Snake',
    },
)
