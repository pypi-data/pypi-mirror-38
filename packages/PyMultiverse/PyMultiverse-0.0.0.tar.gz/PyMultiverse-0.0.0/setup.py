import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyMultiverse",
    version="0.0.0",
    author="Davide Rognoni",
    description="Multi-framework scaffolding tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rognoni/Multiverse",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
