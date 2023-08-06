from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="match_arrays",
    version="0.0.1",
    author="Simon-Martin Schröder",
    author_email="martin.schroeder@nerdluecht.de",
    description="Matching of Numpy arrays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moi90/match_arrays",
    py_modules=['match_arrays'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy'
    ],
)