import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awdtools",
    version="0.0.1b",
    author="Yibai Zhang",
    author_email="xm1994@gmail.com",
    description="Tools for easy CTF AWD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/summershrimp/awdtools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)