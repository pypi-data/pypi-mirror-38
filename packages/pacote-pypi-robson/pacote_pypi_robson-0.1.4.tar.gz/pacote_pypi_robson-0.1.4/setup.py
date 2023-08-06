# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pacote_pypi_robson',
    version='0.1.4',
    url='https://github.com/mstuttgart/codigo-avulso-test-tutorial',
    author='Francisco Robson',
    author_email='email@gmail.com',
    keywords='tutorial pip pacotes robson',
    description='Descrição rapida do que e esse pacote',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[], #instala os pacotes necessarios EX: ['opencv>=1.11']
    data_files=[('pacote_pypi_01',['data/dados.json'])], # arquivos de dados que precisa ser carregado ex: data.json
    test_suite='test',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)