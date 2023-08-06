import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_map",
    version="0.1",
    author="Noah Jadoenathmisier",
    author_email="n.j.m.jadoenathmisier@student.tudelft.nl",
    description="Helper functions for bing static maps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noahiscool13/easy_map",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)