import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eelgraph",
    version="0.0.2",
    author="Wes Taylor",
    author_email="jamsterwes@gmail.com",
    description="creates live chart.js charts from python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jamsterwes/eelgraph",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)
