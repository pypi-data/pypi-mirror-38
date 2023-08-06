import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eye-vision",
    version="0.0.2",
    author="Simbarashe Timothy Motsi",
    author_email="simbamotsi1@gmail.com",
    description="Computer Vision library that makes simple the new powerful.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://simbatmotsi.github.io/eye-vision/",
    packages=setuptools.find_packages(),
    install_requires=['opencv-python', 'matplotlib'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development',
        ],
)