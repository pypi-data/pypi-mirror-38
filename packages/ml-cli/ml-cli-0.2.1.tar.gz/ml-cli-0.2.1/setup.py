from setuptools import setup

setup(
    name='ml-cli',
    description='A group of cli commands that helps with machine learning and docker commands',
    url='https://github.com/devyhia/ml-cli',
    author='Yehya Abouelnaga',
    author_email='yehya.abouelnaga@gmail.com',
    license='MIT',
    keywords='machine learning cli',
    version='0.2.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
        'pyfiglet',
        'clint',
        'pyaml'
    ],
    entry_points='''
        [console_scripts]
        ml-cli=cli:cli
    ''',
)
