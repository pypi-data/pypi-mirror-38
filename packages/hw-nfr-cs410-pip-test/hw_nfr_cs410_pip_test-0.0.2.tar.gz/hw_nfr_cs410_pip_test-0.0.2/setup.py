import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hw_nfr_cs410_pip_test",
    version="0.0.2",
    author="H.W., N.F",
    author_email="norbiein@gmail.com",
    description="Implicit feature mining",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nfreundlich/CS410_CourseProject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
