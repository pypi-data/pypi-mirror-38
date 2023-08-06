import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drivefiller",
    version="2.1.1",
    author="Conor Matthews",
    author_email="conor.matthews15@gmail.com",
    description="A Python 3 library that makes very large files very quickly. Can also return file size.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ConorMatthews/drivefiller",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
