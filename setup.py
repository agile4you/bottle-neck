from distutils.core import setup
import re
import ast


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('bottle_neck/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))


setup(
    name='bottle-neck',
    version=version,
    packages=['bottle_neck'],
    url='https://github.com/agile4you/bottle-neck.git',
    license='GLPv3',
    author='Papavassiliou Vassilis',
    author_email='vpapavasil@gmail.com',
    description='Web services with bottle.py made easy!',
    install_requires=['bottle']
)
