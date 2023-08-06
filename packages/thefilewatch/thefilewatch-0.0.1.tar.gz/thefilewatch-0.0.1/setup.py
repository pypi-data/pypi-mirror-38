from setuptools import setup


setup(
    name='thefilewatch',
    version='0.0.1',
    author='johnlofty',
    author_email='johnlofty@163.com',
    url='https://github.com/johnlofty/thefilewatch',
    description='multi-files watcher',
    packages=['thefilewatch'],
    install_requires=[
        'pyinotify',
    ],
    entry_points={}
)