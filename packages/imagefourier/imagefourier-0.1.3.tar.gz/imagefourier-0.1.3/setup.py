import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imagefourier",
    version="0.1.3",
    author="Athena Parker",
    author_email="neganote43@gmail.com",
    description="Image fourier analysis library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/NegaNote/imagefourier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Pillow",
        "mpmath",
        "numpy",
        "svgpathtools",
        "opencv-python"],
    extras_require={'Cython': ['Cython']}
)
