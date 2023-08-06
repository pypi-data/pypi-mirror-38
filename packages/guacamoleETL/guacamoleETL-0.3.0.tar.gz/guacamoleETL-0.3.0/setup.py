import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="guacamoleETL",
    version="0.3.0",
    author="Chu-Hsuan Lee",
    author_email="joseph.chuhsuanlee@gmail.com",
    description="ETL package for AUTO1 challenge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chuhsuanlee/guacamoleETL",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
