import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    # name='django-myapp',
    name='django-djasync',
    version='0.3',
    packages=['djasync'],
    description='A line of description',
    long_description=README,
    author='Kshitij Mhatre',
    author_email='kshitijpmhatre@gmail.com',
    url='https://github.com/KshitijMhatre/scratchpad/',
    license='MIT',
    install_requires=[
        'Django',
    ]
)
