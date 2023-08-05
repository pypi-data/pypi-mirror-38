import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="putput",
    version="0.0.1",
    author="Michael Perel",
    author_email="michaelsethperel@gmail.com",
    description="Generate utterances by specifying patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaelperel/putput",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
