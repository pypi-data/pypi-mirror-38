import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flyingtrain",
    version="0.1.0",
    author="Chu-Hsuan Lee",
    author_email="joseph.chuhsuanlee@gmail.com",
    description="package for bonial challenge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chuhsuanlee/flyingtrain",
    packages=setuptools.find_packages(),
    install_requires=[
          "ijson==2.3",
      ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
