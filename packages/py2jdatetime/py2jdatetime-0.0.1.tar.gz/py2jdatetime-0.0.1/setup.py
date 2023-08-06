import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py2jdatetime",
    version="0.0.1",
    author="Iddo Yadlin",
    author_email="iddoyadlin@gmail.com",
    description="A package for converting python datetime patterns to java patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Iddoyadlin/Py2JDatetime",
    packages=['py2jdatetime'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
