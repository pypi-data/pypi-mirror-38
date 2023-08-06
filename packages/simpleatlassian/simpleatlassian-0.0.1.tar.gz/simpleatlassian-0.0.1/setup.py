import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpleatlassian",
    version="0.0.1",
    author="Alexander Hungenberg",
    author_email="alexander.hungenberg@gmail.com",
    description="A really basic Atlassian REST Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/defreng/python-simpleatlassian",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
