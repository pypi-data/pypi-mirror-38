import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylio",
    version="0.0.1",
    author="Xavier Collantes",
    author_email="xcollantes@zagmail.gonzaga.edu",
    description="Send emails on command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xcollantes/pylio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)
