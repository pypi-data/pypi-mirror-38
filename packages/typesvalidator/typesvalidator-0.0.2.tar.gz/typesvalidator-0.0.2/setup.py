import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typesvalidator",
    version="0.0.2",
    author="Gustavo Ghioldi",
    author_email="gustavoghioldi@gmail.com",
    description="Validador de tipos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gustavoghioldi/types-validator",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)