import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cknife",
    version="0.0.1",
    author="Yibai Zhang",
    author_email="xm1994@gmail.com",
    description="cknife python module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/summershrimp/cknife",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)