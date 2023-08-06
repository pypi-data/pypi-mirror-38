
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Fus",
    version="0.0.1",
    author="Ben Ayers-Glassey",
    author_email="bayersglassey@gmail.com",
    description="Another little programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bayersglassey/fus2018",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
