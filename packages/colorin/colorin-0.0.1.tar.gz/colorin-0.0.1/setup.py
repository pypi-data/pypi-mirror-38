import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colorin",
    version="0.0.1",
    author="Álvaro García",
    author_email="alvaro.garcia.molino@gmail.com",
    description="Colorea y formatea texto y tablas para salida estandar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gmolino/colorin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
