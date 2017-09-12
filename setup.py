from setuptools import setup
from netbyte import __version__ as VERSION

setup(
    name='netbyte',
    version=VERSION,
    url='http://www.sc0tfree.com',
    license='MIT License',
    author='sc0tfree',
    author_email='henry@sc0tfree.com',
    description='Netbyte is a Netcat-style tool that facilitates probing proprietary TCP and UDP services. It is lightweight, fully interactive and provides formatted output in both hexadecimal and ASCII.',
    keywords='utils cli netcat hexadecimal',
    packages=['netbyte', 'netbyte.util'],
    install_requires=[
        'colorama',
    ],
    entry_points = {
        "console_scripts" : ['netbyte = netbyte.netbyte:main']
    },
)
