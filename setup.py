from distutils.core import setup

setup(
    name='bottle-neck',
    version='1.15',
    packages=['bottle_neck'],
    url='https://github.com/agile4you/bottle-neck.git',
    license='GLPv3',
    author='Papavassiliou Vassilis',
    author_email='vpapavasil@gmail.com',
    description='Web services with bottle.py made easy!',
    extras_require={
        'test': ['pytest', 'bottle', 'six'],
    }
)
