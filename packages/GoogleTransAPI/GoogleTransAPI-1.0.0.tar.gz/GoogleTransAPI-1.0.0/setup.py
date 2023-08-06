import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GoogleTransAPI",
    version="1.0.0",
    author="YunfeiLi",
    description="A package that inputs Japanese and output Mp3 by google translate",
    url="https://github.com/YungfeiLi/GoogleTranApi.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)