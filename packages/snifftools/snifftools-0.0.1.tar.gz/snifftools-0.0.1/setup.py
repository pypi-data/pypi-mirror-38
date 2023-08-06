import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="snifftools",
    version="0.0.1",
    author="Lewis sniff122 Foster",
    author_email="sniff122@sniff122.ga",
    description="A small and simple library for simple python tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sniff122/snifftools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)