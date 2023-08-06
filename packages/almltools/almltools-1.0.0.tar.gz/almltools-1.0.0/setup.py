from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name='almltools',
    version='1.0.0',
    packages=['almltools', 'almltools.core'],
    url='https://github.com/alimcmaster1/al-ml-tools',
    license='Apache License 2.0',
    author='alistair',
    author_email='alimcmaster1@gmail.com',
    description='Alistair McMasters Machine Learning ToolKit',
    install_requires=['pandas'],
    python_requires='>=3',
    # ext_modules = cythonize("almltools/_cython/*.pyx"),
    classifier=[
        'Development Status :: 3 - Alpha'
    ],


)
