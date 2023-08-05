import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fuzzycsv",
    version="0.0.1",
    author="David Roizenman",
    author_email="david@hmnd.io",
    description="Fuzzy matching for CSVs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hmnd/fuzzycsv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Topic :: Utilities",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Intended Audience :: Science/Research",
    ],
)
