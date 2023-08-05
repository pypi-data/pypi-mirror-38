from setuptools import setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='sav',
    version='1.0',
    packages=['sav.info'],
    author='Sander Voerman',
    author_email='sander@savoerman.nl',
    description=long_description.partition('\n')[0],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    python_requires='>=3.7',
    classifiers=[
        'Topic :: Documentation'
    ]
)
