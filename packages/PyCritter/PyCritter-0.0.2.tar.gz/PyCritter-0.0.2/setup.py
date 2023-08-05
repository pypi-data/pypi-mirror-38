import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCritter",
    version="0.0.2",
    author="ArcOnyx",
    author_email="arconyx6@gmail.com",
    description="An API wrapper for CritterDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arconyx/pycritter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
)
