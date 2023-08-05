import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wenviro",
    version="0.0.2",
    author="Gustavo Ghioldi",
    author_email="gustavoghioldir@gmail.com",
    description="Envio variables helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gustavoghioldi/enviro",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)