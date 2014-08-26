from distutils.core import setup

setup(
    name="SciEDPipeR",
    version="0.1.0",
    author="Timothy Tickle, Brian Haas",
    author_email="timothyltickle@gmail.com",
    packages=["SciEDPipeR"],
    scripts=["bin/ExampleScript.py"],
    url="https://github.com/SciEDPipeR/SciEDPipeR",
    license="LICENSE.txt",
    description="Scientific Environment for the Development of Pipeline Resources",
    long_description=open( "README.txt" ).read(),
    install_requires=[],
)
