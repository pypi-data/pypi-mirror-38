import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lemutils",
    version="1.0",
    author="notlem",
    author_email="datjboy@gmail.com",
    description="utils for yeetbot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blankLeM/lemutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Operating System :: OS Independent",
    ],
)