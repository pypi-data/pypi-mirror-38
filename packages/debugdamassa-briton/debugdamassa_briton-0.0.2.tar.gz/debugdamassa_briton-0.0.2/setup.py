import os
from setuptools import setup, find_packages

def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()

setup(
    name='debugdamassa_briton',
    version='0.0.2',
    description='Fatec CI/CD Example',
    # long_description=read('../README.md'),
    url='https://github.com/Lucs1590/TestDebug',
    download_url='https://github.com/Lucs1590/TestDebug',
    license='BSD',
    author='Lucas de Brito Silva',
    author_email='lucasbsilva29@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    keywords=['damassa', 'debug'],
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
    ]
)
