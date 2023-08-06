import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eye-vision",
    version="0.0.0",
    author="Simbarashe Timothy Motsi",
    author_email="simbamotsi1@gmail.com",
    description="Computer Vision library that makes simple the new powerful.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/eye-vision",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
)