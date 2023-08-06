from setuptools import setup

setup(
    name='pydial',
    version='0.2.4',
    packages=['test', 'pydial'],
    url='https://gitlab.sisg.ucl.ac.be/bibsys/pydial',
    license='https://opensource.org/licenses/MIT',
    author='michotter',
    author_email='renaud.michotte@uclouvain.be',
    description='Use DIAL Object with Python',
    install_requires=[
        'eulxml',
        'eulfedora',
        'pymarc',
        'six'
    ]
)
