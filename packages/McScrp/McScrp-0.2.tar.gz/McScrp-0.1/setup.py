import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="McScrp",
    version="0.1",
    author="CHAHBOUN Mohammed",
    author_email="simomega42@gmail.com",
    description="Scraping Library",
    long_description=long_description,
    url="https://github.com/Medpy/McScrp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)