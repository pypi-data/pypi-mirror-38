import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="log_test",
    version="1.0.4",
    author="Liu Li",
    author_email="657013040@qq.com",
    description="A small print test log tool package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ll51668/log",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
