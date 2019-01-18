import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="W7500isp",
    version="0.0.1",
    author="James YS Kim",
    author_email="javakys@gmail.com",
    description="W7500x isp tool package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/javakys/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)