from setuptools import setup, find_packages

setup(
    name='vyapi',
    version='0.1.1',
    description='Python SDK for interacting with VyOS API',
    author='Roberto Berto',
    author_email='roberto.berto@gmail.com',
    url='https://github.com/seu-usuario/vyapi',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
