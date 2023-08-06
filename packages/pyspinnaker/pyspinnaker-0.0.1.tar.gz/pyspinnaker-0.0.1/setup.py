import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyspinnaker",
    version="0.0.1",
    author="Joris De Winne",
    author_email="joris.dewinne@gmail.com",
    description="A python implementation of the Spinnaker API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jdewinne/pyspinnaker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
