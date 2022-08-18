from setuptools import setup, find_packages
import pathlib

current_dir = pathlib.Path(__file__).parent.resolve()
long_description = (current_dir / 'Readme.md').read_text(encoding='utf-8')

setup(
    name="aseq_viv",
    version="0.1dev0",
    description='Asequibilidad vivienda',
    long_description=long_description,
    author='CEEU - UNSAM',
    author_email='fcatalano@unsam.edu.ar',
    url='https://github.com/PyMap/aseq_viv',
    classifiers=[
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(exclude=['*.tests']),
    install_requires=[
        'numpy >= 1.22.2',
        'pandas >= 1.4.1',
        'matplotlib >= 3.4.3',
    ]
)
