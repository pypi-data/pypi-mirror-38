import io
import os.path as op

from setuptools import setup, find_packages

here = op.abspath(op.dirname(__file__))

# Get the long description from the README file
with io.open(op.join(here, 'README.md'), mode='rt', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='knn_kv',
    version='0.0.1',
    description='k-nearest neighbors',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kopylovvlad/knn_kv',
    author='Vladislav Kopylov',
    author_email='kopylov.vlad@gmail.com',
    packages=find_packages(),
    python_requires='>=3.5',
)
