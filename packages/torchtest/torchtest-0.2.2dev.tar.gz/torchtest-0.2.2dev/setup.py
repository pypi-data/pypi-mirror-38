from distutils.core import setup

setup(
    name='torchtest',
    version='0.2.2dev',
    packages=['torchtest',],
    license='License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    long_description=open('README.adoc').read(),
    install_requires=['torch'],
)
