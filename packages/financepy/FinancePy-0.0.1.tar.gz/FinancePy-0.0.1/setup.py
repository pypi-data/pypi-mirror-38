import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FinancePy",
    version="0.0.1",
    author="Dominic O'Kane",
    author_email="dominic.okane@edhec.edu",
    description="A Finance Library",
    long_description="A library of financial functions for pricing and risk managing securities and derivatives",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)