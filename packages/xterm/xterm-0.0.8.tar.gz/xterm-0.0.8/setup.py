import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xterm",
    version="0.0.8",
    author="mat",
    author_email="fake-email@getpranked.lol",
    description="stuff i guess",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://repl.it/@mat1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
