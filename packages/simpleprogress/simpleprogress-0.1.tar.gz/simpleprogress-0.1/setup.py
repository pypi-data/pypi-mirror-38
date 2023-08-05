import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simpleprogress",
    version="0.1",
    description="Simple progress indicator printing to stdout",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(),
    author="Brian Bove",
    author_email="brian@ufmsystems.com",
    keywords=["progress"],
    url="https://github.com/bmbove/simpleprogress",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
