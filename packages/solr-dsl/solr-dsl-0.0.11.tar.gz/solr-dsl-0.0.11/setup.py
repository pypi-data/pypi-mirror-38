import setuptools


with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="solr-dsl",
    version="0.0.11",
    author="Elliot Penson",
    author_email="elliotpenson@gmail.com",
    description="Python client for Solr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/it-com-engineering/solr-dsl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
