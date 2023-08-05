import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysnowball",
    version="0.0.1",
    author="Yang Yu",
    author_email="yang.lights@hotmail.com",
    description="xueqiu api python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uname-yang/pysnowball",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
