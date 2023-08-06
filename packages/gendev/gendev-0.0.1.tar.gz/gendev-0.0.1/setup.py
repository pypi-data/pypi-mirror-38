import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gendev",
    version="0.0.1",
    author="James Whiteman",
    author_email="james.whiteman@genunity.co.nz",
    description="AWS IoT device factory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
       "console_scripts": ["gendev=gendev.gendev:main"],
    },
)
